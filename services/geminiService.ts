import { GoogleGenAI, Chat, Type } from "@google/genai";
import { PracticalCase, GroundingSource, MindMapNode, StudyPlanInput, MockExam, Flashcard, PracticalCaseQuestion } from '../types';

if (!process.env.API_KEY) {
    throw new Error("API_KEY environment variable not set");
}

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

const caseGeneratorModel = 'gemini-2.5-pro';
const chatModel = 'gemini-2.5-flash';
const searchModel = 'gemini-2.5-flash';
const creativeModel = 'gemini-2.5-pro';
const imageModel = 'imagen-4.0-generate-001';


const practicalCaseQuestionSchema = {
    type: Type.OBJECT,
    properties: {
        id: { type: Type.STRING, description: "A unique identifier for the question, e.g., 'q1', 'q2'."},
        question: { type: Type.STRING, description: "The specific question the user must answer based on the scenario." },
        options: {
            type: Type.ARRAY,
            description: "An array of 4 multiple choice options.",
            items: {
                type: Type.OBJECT,
                properties: {
                    id: { type: Type.STRING, description: "A unique identifier for the option, e.g., 'A', 'B', 'C', 'D'." },
                    text: { type: Type.STRING, description: "The text of the option." }
                },
                required: ["id", "text"],
            }
        },
        correct_option_id: { type: Type.STRING, description: "The ID of the correct option." },
        explanation: { type: Type.STRING, description: "A detailed explanation of why the correct option is right and the others are wrong, citing relevant articles if possible." }
    },
    required: ["id", "question", "options", "correct_option_id", "explanation"]
};

const practicalCaseSchema = {
    type: Type.OBJECT,
    properties: {
        topic: { type: Type.STRING, description: "The legal topic of the case, e.g., 'Incapacidad Temporal'." },
        scenario: { type: Type.STRING, description: "A detailed and complex scenario describing the practical case." },
        questions: {
            type: Type.ARRAY,
            description: "An array of 5 challenging multiple-choice questions related to the scenario.",
            items: practicalCaseQuestionSchema,
        }
    },
    required: ["topic", "scenario", "questions"],
};

export async function generatePracticalCase(): Promise<PracticalCase> {
    const prompt = `Act as an expert examiner for the Spanish Social Security civil service exam. Your task is to create a high-quality 'supuesto práctico'.
Follow these instructions precisely:
1.  **Choose a Topic**: Select a relevant, specific topic from Spanish Social Security law (e.g., Jubilación parcial, Cotización en pluriempleo, Prestación por riesgo durante el embarazo).
2.  **Create a Scenario**: Write a detailed, realistic, and complex scenario based on the chosen topic. Include specific dates, names, figures, and circumstances that are crucial for answering the questions. The scenario must be based on current Spanish legislation.
3.  **Generate 5 Questions**: Based ONLY on the scenario provided, create exactly 5 distinct multiple-choice questions. Each question must be challenging and require careful analysis of the scenario.
4.  **Provide 4 Options per Question**: For each question, create four plausible options (A, B, C, D). Only one option can be correct.
5.  **Identify Correct Answer and Explain**: For each question, clearly identify the correct option ID and provide a thorough legal explanation, citing the specific articles of the relevant laws (e.g., Real Decreto Legislativo 8/2015) that justify the answer.

You MUST return the output in a clean, valid JSON format that adheres to the provided schema.`;
    
    try {
        const response = await ai.models.generateContent({
            model: caseGeneratorModel,
            contents: prompt,
            config: {
                responseMimeType: "application/json",
                responseSchema: practicalCaseSchema,
                thinkingConfig: { thinkingBudget: 32768 },
                temperature: 0.4,
            },
        });
        
        const jsonText = response.text.trim();
        const parsedJson = JSON.parse(jsonText);
        
        if (!parsedJson.topic || !parsedJson.scenario || !Array.isArray(parsedJson.questions) || parsedJson.questions.length === 0) {
            console.error("API returned invalid format for practical case:", parsedJson);
            throw new Error("Invalid format for practical case received from API.");
        }

        // Ensure questions array is correctly typed
        return {
            ...parsedJson,
            questions: parsedJson.questions as PracticalCaseQuestion[]
        } as PracticalCase;

    } catch (error) {
        console.error("Error generating practical case:", error);
        throw new Error("Failed to generate a new practical case. The model may be experiencing high load. Please try again in a moment.");
    }
}

let chatInstances: { [key: string]: Chat } = {};

export function getChatInstance(conversationId: string): Chat {
    if (!chatInstances[conversationId]) {
        chatInstances[conversationId] = ai.chats.create({
            model: chatModel,
            config: {
                systemInstruction: `You are a world-class expert tutor specializing in Spanish Social Security legislation for civil service exam candidates ('opositores'). Your tone is encouraging, precise, and clear. When a user asks a question, provide a direct and accurate answer. If they present a problem or a practical case, break down the explanation step-by-step, citing relevant legal articles (e.g., from the 'Real Decreto Legislativo 8/2015') whenever possible. Your goal is to help the user understand complex legal concepts, not just give them the answer.`
            }
        });
    }
    return chatInstances[conversationId];
}

export async function searchWithGrounding(query: string, untilDate?: string): Promise<{ text: string, sources: GroundingSource[] }> {
    try {
        let finalQuery = query;
        if (untilDate) {
            try {
                const formattedDate = new Date(untilDate).toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });
                finalQuery += ` (Important: all information and legislation cited must be effective on or before ${formattedDate})`;
            } catch (dateError) {
                console.error("Invalid date provided:", untilDate);
            }
        }

        const response = await ai.models.generateContent({
            model: searchModel,
            contents: finalQuery,
            config: {
                tools: [{ googleSearch: {} }],
            },
        });

        const text = response.text;
        const rawChunks = response.candidates?.[0]?.groundingMetadata?.groundingChunks || [];
        
        const sources: GroundingSource[] = rawChunks
            .map(chunk => chunk.web)
            .filter(web => web && web.uri && web.title)
            .map(web => ({ uri: web.uri!, title: web.title! }));

        return { text, sources };
    } catch (error) {
        console.error("Error with grounded search:", error);
        throw new Error("Failed to perform the search. Please check your query and try again.");
    }
}
  
export async function generateMindMap(topic: string): Promise<MindMapNode> {
    const prompt = `Generate a hierarchical mind map about the following Spanish legislation topic: "${topic}".
The structure must be logical for studying. Create a single root node and at least two levels of nested child nodes.
You MUST provide the output in a clean, valid JSON format.
The JSON must represent the node tree. Each node must be an object with three properties:
1. "id": a unique string identifier (e.g., "root", "1.1", "1.1.2").
2. "text": a string containing the concept or idea.
3. "children": an array of node objects.

Example of expected JSON structure:
{
  "id": "root",
  "text": "Main Topic",
  "children": [
    {
      "id": "1",
      "text": "Sub-Topic 1",
      "children": [
        { "id": "1.1", "text": "Detail A", "children": [] }
      ]
    }
  ]
}

Do not include any text or markdown formatting outside of the main JSON object.`;

    try {
        const response = await ai.models.generateContent({
            model: creativeModel,
            contents: prompt,
            config: {
                responseMimeType: "application/json",
                responseSchema: {
                    type: Type.OBJECT,
                    properties: {
                        id: { type: Type.STRING },
                        text: { type: Type.STRING },
                        children: { 
                            type: Type.ARRAY,
                            items: {
                                type: Type.OBJECT,
                                properties: {
                                    id: { type: Type.STRING },
                                    text: { type: Type.STRING },
                                    children: { type: Type.ARRAY, items: { type: Type.OBJECT } } // Simplified for deeper nesting
                                }
                            }
                        }
                    }
                }
            }
        });
        
        let jsonText = response.text.trim();
        const parsed = JSON.parse(jsonText);
        return parsed as MindMapNode;
    } catch (error) {
        console.error("Error generating mind map:", error);
        throw new Error("Failed to generate mind map. The model might have returned an invalid format. Please try again.");
    }
}

export async function generateStudyPlan(input: StudyPlanInput): Promise<string> {
    const { availability, duration, includeTracking, includeSuggestions } = input;

    let prompt = `Create a ${duration} study plan for a Spanish Social Security civil service exam candidate.
    Availability: ${availability}.
    The plan should be structured, realistic, and cover key areas of the syllabus. 
    Format the output as Markdown. Use headings for days or weeks, and bullet points for tasks.
    Include a balance of theory study, practical cases, and review sessions.`;

    if (includeTracking) {
        prompt += "\nInclude a checkbox column `[ ]` for each task so the user can track their progress."
    }
    if (includeSuggestions) {
        prompt += "\nAt the end of each week/major section, add a 'Sugerencia IA' block with a proactive tip, like suggesting a specific law to review or a complex topic to focus on."
    }

    try {
        const response = await ai.models.generateContent({
            model: creativeModel,
            contents: prompt,
        });
        return response.text;
    } catch (error) {
        console.error("Error generating study plan:", error);
        throw new Error("Failed to generate study plan.");
    }
}

export async function generateSchema(topic: string): Promise<string> {
    const prompt = `Act as an expert legal tutor. Create a clear, hierarchical, and well-structured outline (esquema) on the following topic from Spanish law: "${topic}".
    Use Markdown formatting with nested bullet points to represent the hierarchy.
    The outline must be detailed enough to be a useful study guide, covering key definitions, requirements, procedures, and relevant concepts.`;

    try {
        const response = await ai.models.generateContent({
            model: creativeModel,
            contents: prompt,
        });
        return response.text;
    } catch (error) {
        console.error("Error generating schema:", error);
        throw new Error("Failed to generate schema.");
    }
}

export async function generateSummary(text: string): Promise<string> {
    const prompt = `Act as an expert legal analyst. Read the following legal text and provide a concise summary.
    The summary should capture the main points, key articles, and essential conclusions of the text.
    Format the output in clear, easy-to-read paragraphs using Markdown.

    Text to summarize:
    ---
    ${text}
    ---`;

    try {
        const response = await ai.models.generateContent({
            model: creativeModel,
            contents: prompt,
        });
        return response.text;
    } catch (error) {
        console.error("Error generating summary:", error);
        throw new Error("Failed to generate summary.");
    }
}

export async function compareLawVersions(textA: string, textB: string): Promise<string> {
    const prompt = `Act as an expert legislative analyst. I will provide you with two versions of a legal text, "Text A (Old Version)" and "Text B (New Version)".
    Your task is to compare them and produce a clear, structured report of the differences.
    The report should be formatted in Markdown and include:
    1.  A general summary of the main changes.
    2.  A section for "Modifications", detailing what has been changed in existing articles.
    3.  A section for "Additions", listing new articles or significant new clauses.
    4.  A section for "Deletions", listing parts that were in Text A but not in Text B.

    Be precise and focus on the substantive changes.

    ---
    Text A (Old Version):
    ${textA}
    ---
    Text B (New Version):
    ${textB}
    ---`;

    try {
        const response = await ai.models.generateContent({
            model: creativeModel,
            contents: prompt,
        });
        return response.text;
    } catch (error) {
        console.error("Error comparing texts:", error);
        throw new Error("Failed to compare law versions.");
    }
}

// NOTE: In a real-world application, this would call a backend service/proxy
// to fetch the URL content to avoid CORS issues in the browser.
export async function getTextFromUrl(url: string): Promise<string> {
    console.warn("Using a simplified client-side fetch. This may fail due to CORS. A backend proxy is recommended for production.");
    try {
        // A simple proxy could be used, e.g., 'https://cors-anywhere.herokuapp.com/' + url
        // For this example, we assume direct access or a browser extension handles CORS.
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        // This is a very basic text extraction and won't work well for complex sites.
        // A proper backend would use a library like Cheerio or JSDOM to parse HTML.
        return await response.text();
    } catch (error) {
        console.error("Failed to fetch URL content:", error);
        throw new Error("No se pudo obtener el contenido de la URL. Esto puede deberse a restricciones de CORS. Se recomienda un proxy de backend.");
    }
}

export async function generateMockExam(topics: string[], questionCount: number): Promise<MockExam> {
     const prompt = `Act as an expert examiner for the Spanish Social Security civil service exam. Create a complete mock exam ('simulacro').
Instructions:
1.  **Title**: The exam title should be "Simulacro de Examen - Seguridad Social".
2.  **Topics**: The exam must exclusively cover the following topics: ${topics.join(', ')}.
3.  **Question Count**: Generate exactly ${questionCount} multiple-choice questions.
4.  **Structure**: For each question, create a small, realistic scenario OR a direct question about the topics. Then provide 4 plausible options (A, B, C, D) and identify the correct one, along with a detailed legal explanation citing relevant articles.
5.  **Variety**: Ensure a good mix of questions covering all specified topics.

You MUST return the output in a clean, valid JSON format.`;
    
    // Create a dynamic schema for the questions array
    const examSchema = {
        type: Type.OBJECT,
        properties: {
            title: { type: Type.STRING },
            questions: {
                type: Type.ARRAY,
                description: `An array of exactly ${questionCount} questions.`,
                items: practicalCaseQuestionSchema,
            }
        },
        required: ["title", "questions"]
    };

    try {
        const response = await ai.models.generateContent({
            model: caseGeneratorModel, // Use the powerful model for this complex task
            contents: prompt,
            config: {
                responseMimeType: "application/json",
                responseSchema: examSchema,
                thinkingConfig: { thinkingBudget: 32768 }
            },
        });

        const jsonText = response.text.trim();
        const parsedJson = JSON.parse(jsonText);

        if (!parsedJson.title || !Array.isArray(parsedJson.questions)) {
            throw new Error("Invalid format for mock exam received from API.");
        }
        return parsedJson as MockExam;

    } catch (error) {
        console.error("Error generating mock exam:", error);
        throw new Error("Failed to generate mock exam. Please try again.");
    }
}

export async function generateFlashcardsAndMeme(topic: string): Promise<{ flashcards: Flashcard[], meme: { imageUrl: string, prompt: string } }> {
    const flashcardSchema = {
        type: Type.OBJECT,
        properties: {
            flashcards: {
                type: Type.ARRAY,
                description: "An array of 5-10 flashcards.",
                items: {
                    type: Type.OBJECT,
                    properties: {
                        id: { type: Type.STRING },
                        front: { type: Type.STRING, description: "The front of the card (a question or term)." },
                        back: { type: Type.STRING, description: "The back of the card (the answer or definition)." }
                    },
                    required: ["id", "front", "back"]
                }
            },
            meme_prompt: {
                type: Type.STRING,
                description: "A short, witty, and visually descriptive prompt to generate a funny meme related to the topic. For example: 'A photo of a stressed person buried under a mountain of paperwork, with the caption: Trying to calculate the base reguladora'."
            }
        },
        required: ["flashcards", "meme_prompt"]
    };

    const flashcardPrompt = `Generate a set of study flashcards and a meme idea for the Spanish legal topic: "${topic}".
1.  **Flashcards**: Create 5 to 10 high-quality flashcards. Each should have a 'front' (a clear question or key term) and a 'back' (a concise and accurate answer or definition).
2.  **Meme Prompt**: Create a short, funny, and descriptive prompt for an image generation model to create a meme about this topic. It should be relatable to someone studying for the exam.

Return the result as a single, valid JSON object.`;

    try {
        // Step 1: Generate flashcards and meme prompt text
        const textResponse = await ai.models.generateContent({
            model: creativeModel,
            contents: flashcardPrompt,
            config: {
                responseMimeType: "application/json",
                responseSchema: flashcardSchema,
            }
        });
        const parsedText = JSON.parse(textResponse.text.trim());
        const flashcards: Flashcard[] = parsedText.flashcards;
        const memePrompt: string = parsedText.meme_prompt;

        // Step 2: Generate the image for the meme
        const imageResponse = await ai.models.generateImages({
            model: imageModel,
            prompt: memePrompt,
            config: {
                numberOfImages: 1,
                outputMimeType: 'image/jpeg',
                aspectRatio: '1:1',
            }
        });
        const base64ImageBytes: string = imageResponse.generatedImages[0].image.imageBytes;
        const imageUrl = `data:image/jpeg;base64,${base64ImageBytes}`;

        return { flashcards, meme: { imageUrl, prompt: memePrompt } };
    } catch (error) {
        console.error("Error generating flashcards/meme:", error);
        throw new Error("Failed to generate flashcards and meme.");
    }
}
