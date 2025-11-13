
import React from 'react';

const APIKeyInput: React.FC<{ provider: string, isConfigured: boolean }> = ({ provider, isConfigured }) => (
    <div>
        <label htmlFor={`${provider}-key`} className="block text-sm font-medium text-slate-700 dark:text-slate-300">{provider} API Key</label>
        <div className="mt-1 flex rounded-md shadow-sm">
             <span className={`inline-flex items-center px-3 rounded-l-md border border-r-0 ${isConfigured ? 'bg-green-100 border-green-300 text-green-700 dark:bg-green-900/50 dark:border-green-700 dark:text-green-300' : 'bg-slate-100 border-slate-300 text-slate-500 dark:bg-slate-800 dark:border-slate-600 dark:text-slate-400'}`}>
                {isConfigured ? 'Configurada' : 'No Configurada'}
            </span>
            <input 
                type="password" 
                id={`${provider}-key`}
                placeholder="••••••••••••••••••••••••••"
                disabled 
                className="flex-1 block w-full rounded-none rounded-r-md bg-slate-200 dark:bg-slate-700 border-slate-300 dark:border-slate-600 cursor-not-allowed sm:text-sm"
            />
        </div>
    </div>
);


const SettingsView: React.FC = () => {
    return (
        <div className="flex flex-col h-full bg-white dark:bg-slate-900">
            <header className="p-4 border-b border-slate-200 dark:border-slate-800">
                <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Configuración</h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">Gestiona tus preferencias y claves de API.</p>
            </header>
            
            <div className="flex-1 overflow-y-auto p-6 lg:p-8">
                <div className="max-w-4xl mx-auto space-y-12">
                    
                    <div>
                        <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-200">Gestionar Claves de API (Bring Your Own Key)</h2>
                        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Esta funcionalidad está en desarrollo. Próximamente podrás conectar tus propias claves de API para un uso ilimitado.</p>
                        <div className="mt-6 space-y-4">
                            <APIKeyInput provider="Google Gemini" isConfigured={!!process.env.API_KEY} />
                            <APIKeyInput provider="OpenAI (GPT-4)" isConfigured={false} />
                            <APIKeyInput provider="Anthropic (Claude)" isConfigured={false} />
                            <APIKeyInput provider="Mistral AI" isConfigured={false} />
                        </div>
                         <div className="mt-6 text-right">
                            <button disabled className="px-4 py-2 bg-slate-300 text-slate-500 rounded-lg font-semibold cursor-not-allowed">Guardar Cambios</button>
                        </div>
                    </div>
                    
                    <div>
                        <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-200">Ideas de Monetización y Modelo de Negocio</h2>
                         <div className="mt-4 p-4 bg-amber-50 dark:bg-amber-900/40 border-l-4 border-amber-400 rounded-r-lg">
                            <p className="text-sm text-amber-800 dark:text-amber-200 leading-relaxed">
                                El mercado de opositores en España es muy competitivo pero también muy dispuesto a invertir en herramientas de calidad. Un modelo <strong>Freemium</strong> es ideal para captar una base amplia de usuarios y luego convertir a los más comprometidos.
                            </p>
                             <ul className="mt-3 list-disc pl-5 text-sm text-amber-700 dark:text-amber-300 space-y-1">
                                <li><strong>Plan Gratuito:</strong> Acceso a todas las herramientas pero con límites de uso diarios (ej: 10 mensajes de chat, 2 casos prácticos, 1 mapa mental al día). Suficiente para probar el valor de la app.</li>
                                <li><strong>Plan PRO (Suscripción Mensual/Anual):</strong> Acceso ilimitado a todas las funcionalidades, historial de progreso extendido, y quizás acceso a modelos de IA más potentes (como Gemini 2.5 Pro para todo). El precio podría rondar los 9-15€/mes, un coste muy competitivo frente a academias tradicionales.</li>
                                <li><strong>Opción "Bring Your Own Key":</strong> Permitir que los usuarios PRO usen su propia clave de API les da control total sobre su consumo y puede ser un gran atractivo para usuarios avanzados.</li>
                            </ul>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default SettingsView;
