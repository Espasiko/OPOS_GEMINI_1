import React, { useState, useCallback } from 'react';
import { UploadIcon } from './icons/UploadIcon';
import { LinkIcon } from './icons/LinkIcon';
import { SparkIcon } from './icons/SparkIcon';

declare const pdfjsLib: any;

export async function extractTextFromFile(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = async (event) => {
            try {
                if (file.type === 'application/pdf') {
                    const typedarray = new Uint8Array(event.target?.result as ArrayBuffer);
                    const pdf = await pdfjsLib.getDocument(typedarray).promise;
                    let text = '';
                    for (let i = 1; i <= pdf.numPages; i++) {
                        const page = await pdf.getPage(i);
                        const content = await page.getTextContent();
                        text += content.items.map((item: any) => item.str).join(' ');
                    }
                    resolve(text);
                } else { // txt, md, etc.
                    resolve(event.target?.result as string);
                }
            } catch (error) {
                reject(new Error('Error al procesar el archivo.'));
            }
        };
        reader.onerror = () => reject(new Error('Error al leer el archivo.'));

        if (file.type === 'application/pdf') {
            reader.readAsArrayBuffer(file);
        } else {
            reader.readAsText(file);
        }
    });
}


interface InputSourceSelectorProps {
    onTextSubmit: (source: { type: 'text'; content: string } | { type: 'file'; content: File } | { type: 'url'; content: string }) => void;
    isLoading: boolean;
    error: string | null;
    initialText?: string;
    showTextField?: boolean;
    textAreaRows?: number;
}

const InputSourceSelector: React.FC<InputSourceSelectorProps> = ({ onTextSubmit, isLoading, error, initialText = '', showTextField = true, textAreaRows = 15 }) => {
    const [activeTab, setActiveTab] = useState(showTextField ? 'text' : 'file');
    const [textValue, setTextValue] = useState(initialText);
    const [urlValue, setUrlValue] = useState('');
    const [fileValue, setFileValue] = useState<File | null>(null);
    const [fileName, setFileName] = useState('');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setFileValue(file);
            setFileName(file.name);
        }
    };
    
    const handleSubmit = () => {
        if (activeTab === 'text' && textValue.trim()) {
            onTextSubmit({ type: 'text', content: textValue });
        } else if (activeTab === 'file' && fileValue) {
            onTextSubmit({ type: 'file', content: fileValue });
        } else if (activeTab === 'url' && urlValue.trim()) {
            onTextSubmit({ type: 'url', content: urlValue });
        }
    }

    const isSubmitDisabled = isLoading || (activeTab === 'text' && !textValue.trim()) || (activeTab === 'file' && !fileValue) || (activeTab === 'url' && !urlValue.trim());

    return (
        <div className="w-full bg-slate-50 dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700 p-1">
            <div className="flex border-b border-slate-200 dark:border-slate-700">
                {showTextField && <TabButton label="Texto" isActive={activeTab === 'text'} onClick={() => setActiveTab('text')} />}
                <TabButton label="Subir Archivo" isActive={activeTab === 'file'} onClick={() => setActiveTab('file')} />
                <TabButton label="Desde URL" isActive={activeTab === 'url'} onClick={() => setActiveTab('url')} />
            </div>
            <div className="p-4">
                {activeTab === 'text' && showTextField && (
                     <textarea
                        value={textValue}
                        onChange={(e) => setTextValue(e.target.value)}
                        placeholder="Pega aquí el texto..."
                        rows={textAreaRows}
                        className="w-full p-2 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-md text-sm"
                    />
                )}
                {activeTab === 'file' && (
                    <div className="flex items-center justify-center w-full">
                        <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-32 border-2 border-slate-300 dark:border-slate-600 border-dashed rounded-lg cursor-pointer bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600">
                            <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                <UploadIcon className="w-8 h-8 mb-2 text-slate-500 dark:text-slate-400"/>
                                <p className="mb-1 text-sm text-slate-500 dark:text-slate-400"><span className="font-semibold">Haz clic para subir</span> o arrastra y suelta</p>
                                <p className="text-xs text-slate-500 dark:text-slate-400">PDF, TXT, MD</p>
                            </div>
                            <input id="dropzone-file" type="file" className="hidden" onChange={handleFileChange} accept=".pdf,.txt,.md" />
                        </label>
                    </div>
                )}
                 {activeTab === 'url' && (
                    <div className="relative">
                        <LinkIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400"/>
                        <input
                            type="url"
                            value={urlValue}
                            onChange={(e) => setUrlValue(e.target.value)}
                            placeholder="https://www.boe.es/..."
                            className="w-full p-2 pl-10 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-md text-sm"
                        />
                    </div>
                )}

                {fileName && activeTab === 'file' && (
                    <div className="mt-2 text-sm text-center text-slate-600 dark:text-slate-300">Archivo seleccionado: <strong>{fileName}</strong></div>
                )}

                {showTextField && (
                    <button onClick={handleSubmit} disabled={isSubmitDisabled} className="mt-4 w-full px-4 py-2 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 disabled:bg-slate-400 flex items-center justify-center gap-2">
                        {isLoading ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> : <SparkIcon className="w-5 h-5"/>}
                        <span>{isLoading ? 'Procesando...' : 'Enviar a la IA'}</span>
                    </button>
                )}

                {error && <div className="mt-2 text-sm text-red-500 text-center">{error}</div>}
            </div>
        </div>
    );
}

const TabButton: React.FC<{label: string, isActive: boolean, onClick: () => void}> = ({ label, isActive, onClick }) => (
    <button
        onClick={onClick}
        className={`px-4 py-2 text-sm font-medium transition-colors ${
            isActive
                ? 'border-b-2 border-blue-500 text-blue-600 dark:text-blue-400'
                : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50'
        }`}
    >
        {label}
    </button>
);


export default InputSourceSelector;
