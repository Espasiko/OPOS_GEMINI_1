
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
                        </ul>
                    </Section>

                    <Section title="Generador de Casos">
                        <p>La herramienta definitiva para practicar. Cada vez que pulsas "Nuevo Caso", la IA crea un escenario práctico complejo y 5 preguntas tipo test, imitando el formato del examen oficial.</p>
                        <p>Tienes <strong>dos intentos</strong> por pregunta. Si fallas el primero, puedes volver a intentarlo. Tras el segundo intento o al acertar, se revelará la explicación detallada para que aprendas del error.</p>
                    </Section>

                    <Section title="Búsqueda Actualizada">
                        <p>¿Necesitas información legislativa vigente y contrastada? Esta herramienta utiliza Google Search para fundamentar sus respuestas en información web reciente.</p>
                        <p><strong>Consejo Pro:</strong> Usa el filtro de fecha para limitar la búsqueda a la legislación vigente en la fecha de tu convocatoria. Esto es crucial para no estudiar con normativa derogada o posterior.</p>
                    </Section>
                    
                    <Section title="Temario Oficial">
                        <p>Accede al temario completo y estructurado. Cada tema es desplegable y contiene enlaces directos a la legislación fundamental asociada en el BOE. Es tu índice de estudio interactivo.</p>
                    </Section>

                    <Section title="Mapas Mentales">
                        <p>Una forma visual y efectiva de estructurar y memorizar información. Introduce un tema (ej: "El Recurso de Alzada") y la IA creará un mapa mental jerárquico. Puedes editar el texto de cada idea, descargarlo en formato JSON para usarlo en otras apps, o compartirlo.</p>
                    </Section>
                    
                    <Section title="Plan de Estudios">
                        <p>Organiza tu tiempo de forma eficiente. Indica tu disponibilidad y preferencias, y la IA diseñará un plan de estudio realista y equilibrado. El plan generado es totalmente editable, así que puedes ajustarlo a tus necesidades.</p>
                    </Section>
                    
                     <Section title="Mi Progreso">
                        <p>Mide tu evolución de forma objetiva. Esta sección registra tus aciertos y fallos en el Generador de Casos y te los muestra en gráficos claros. Analiza tus estadísticas para saber dónde debes reforzar y mantén la motivación con los mensajes de ánimo personalizados.</p>
                    </Section>

                </div>
            </div>
        </div>
    );
};

export default UserGuideView;
