import { useState, useEffect } from 'react'

// Componente para mostrar instrucciones de navegación paso a paso
const NavigationInstructions = ({ route }) => {
  const [currentStep, setCurrentStep] = useState(0)

  if (!route || !route.route || !route.route.legs || !route.route.legs[0]) {
    return null
  }

  const steps = route.route.legs[0].steps || []
  const currentInstruction = steps[currentStep]

  useEffect(() => {
    // Simulación: avanzar automáticamente cada 10 segundos
    if (steps.length > 0) {
      const interval = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev < steps.length - 1) {
            return prev + 1
          }
          return prev
        })
      }, 10000) // 10 segundos

      return () => clearInterval(interval)
    }
  }, [steps.length])

  if (steps.length === 0) return null

  return (
    <div className="absolute bottom-4 left-4 right-4 z-20">
      <div className="bg-white/95 backdrop-blur-sm rounded-lg p-4 shadow-lg">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center font-bold">
            {currentStep + 1}
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-800 mb-1">
              {currentInstruction?.instructions || 'Sigue la ruta'}
            </p>
            <p className="text-xs text-gray-500">
              Paso {currentStep + 1} de {steps.length}
            </p>
          </div>
        </div>

        {/* Barra de progreso */}
        <div className="mt-3 h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-orange-500 transition-all duration-300"
            style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
          />
        </div>

        {/* Botones de navegación */}
        <div className="flex gap-2 mt-3">
          <button
            onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
            disabled={currentStep === 0}
            className="flex-1 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-200"
          >
            ← Anterior
          </button>
          <button
            onClick={() => setCurrentStep(Math.min(steps.length - 1, currentStep + 1))}
            disabled={currentStep === steps.length - 1}
            className="flex-1 px-3 py-2 bg-orange-500 text-white rounded-lg text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-orange-600"
          >
            Siguiente →
          </button>
        </div>
      </div>
    </div>
  )
}

export default NavigationInstructions

