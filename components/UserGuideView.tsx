

import React from 'react';

const Section: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
    <div className="mb-6">
        <h2 className="text-2xl font-bold mb-3 text-slate-800 dark:text-slate-100 border-b-2 border-blue-500 pb-2">{title}</h2>
        <div className="prose prose-slate dark:prose-invert max-w-none leading-relaxed">
            {children}
        </div>
    </div>
);

const UserGuideView: React.FC = () => {
    return (
        <div className="flex flex-col h-full bg-white dark:bg-slate-900">
            <header className="p-4 border-b border-slate-200 dark:border-slate-800">
                <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Guía de Uso</h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">Saca el máximo partido a tu asistente de estudio OpositaIA.</p>
            </header>
            
            <div className="flex-1 overflow-y-auto p-6 lg:p-8">
                <div className="max-w-4xl mx-auto">
                    <Section title="Chat Explicativo">
                        <p>Tu tutor personal disponible 24/7. Utilízalo para:</p>
                        <ul>
                            <li>Resolver dudas concretas sobre legislación.</li>
                            <li>Pedir que te explique conceptos complejos de forma sencilla.</li>
                            <li>Analizar un artículo de una ley.</li>
                            <li>Crear un historial de conversaciones para repasar tus dudas más frecuentes.</li>
                             <li>Puedes subir documentos (PDF, TXT) o pegar URLs para que el chat analice el contenido y responda a tus preguntas sobre él.</li>
                        </ul>
                    </Section>

                    <Section title="Generador de Casos">
                        <p>La herramienta para la práctica diaria. Cada vez que pulsas "Nuevo Caso", la IA crea un escenario práctico complejo y 5 preguntas tipo test, imitando el formato del examen oficial.</p>
                        <p>Tienes <strong>dos intentos</strong> por pregunta. Si fallas el primero, puedes volver a intentarlo. Tras el segundo intento o al acertar, se revelará la explicación detallada para que aprendas del error.</p>
                    </Section>

                    <Section title="Simulacros de Examen">
                        <p>Prepara el día del examen en condiciones reales. Esta herramienta te permite:</p>
                        <ul>
                            <li><strong>Configurar tu examen:</strong> Elige los temas específicos que quieres incluir y el número de preguntas.</li>
                            <li><strong>Contrarreloj:</strong> Realiza el examen con un tiempo límite (90 segundos por pregunta) para simular la presión real.</li>
                            <li><strong>Revisión detallada:</strong> Al finalizar, obtendrás tu nota y podrás revisar cada pregunta, viendo tu respuesta, la correcta y una explicación legal completa.</li>
                        </ul>
                    </Section>

                    <Section title="Búsqueda Actualizada">
                        <p>¿Necesitas información legislativa vigente y contrastada? Esta herramienta utiliza Google Search para fundamentar sus respuestas en información web reciente.</p>
                        <p><strong>Consejo Pro:</strong> Usa el filtro de fecha para limitar la búsqueda a la legislación vigente en la fecha de tu convocatoria. Esto es crucial para no estudiar con normativa derogada o posterior.</p>
                    </Section>
                    
                    <Section title="Temario Oficial">
                        <p>Accede al temario completo y estructurado. Cada tema es desplegable y contiene enlaces directos a la legislación fundamental asociada en el BOE. Es tu índice de estudio interactivo.</p>
                    </Section>

                    <Section title="Mapas Mentales">
                        <p>Una forma visual y efectiva de estructurar y memorizar información. Introduce un tema (ej: "El Recurso de Alzada") y la IA creará un mapa mental jerárquico. Puedes editar el texto de cada idea haciendo doble clic y descargarlo en formato PNG, Markdown o JSON.</p>
                    </Section>

                    <Section title="Esquemas">
                        <p>Perfecto para obtener una vista estructurada de un tema. Introduce un concepto o el nombre de una ley y la IA generará un esquema detallado con puntos y subpuntos, ideal para repasar la estructura de la materia.</p>
                    </Section>

                    <Section title="Resúmenes">
                        <p>Ahorra tiempo de lectura. Pega un texto largo, sube un documento PDF/TXT o introduce una URL, y la IA extraerá las ideas clave, creando un resumen conciso y fácil de entender.</p>
                    </Section>

                    <Section title="Comparador de Leyes">
                        <p>¿Ha cambiado una ley y no sabes qué es diferente? Carga la versión antigua y la nueva del texto (desde archivo, URL o pegando el texto) y la IA generará un informe detallado con las modificaciones, adiciones y eliminaciones.</p>
                    </Section>
                    
                    <Section title="Tarjetas y Memes">
                         <p>Refuerza la memoria de forma divertida. Introduce un tema y la IA creará un conjunto de "flashcards" interactivas (pregunta y respuesta) y un meme relacionado con el tema para ayudarte a fijar conceptos de una manera más amena.</p>
                    </Section>
                    
                    <Section title="Plan de Estudios">
                        <p>Organiza tu tiempo de forma eficiente. Indica tu disponibilidad y preferencias, y la IA diseñará un plan de estudio realista y equilibrado. El plan generado es totalmente editable, así que puedes ajustarlo a tus necesidades.</p>
                    </Section>
                    
                     <Section title="Mi Progreso">
                        <p>Mide tu evolución de forma objetiva. Esta sección registra tus aciertos y fallos en el Generador de Casos y en los Simulacros, y te los muestra en gráficos claros. Analiza tus estadísticas para saber dónde debes reforzar y mantén la motivación con los mensajes de ánimo personalizados.</p>
                    </Section>

                </div>
            </div>
        </div>
    );
};

export default UserGuideView;