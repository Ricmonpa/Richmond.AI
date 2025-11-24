import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import MapContainer from '../components/Map/MapContainer'
import NavigationInstructions from '../components/NavigationInstructions'

// Página de navegación con mapa y ruta
const NavigationPage = () => {
  const { selectedRoute, destination } = useApp()
  const navigate = useNavigate()

  if (!selectedRoute) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">No hay ruta seleccionada</p>
          <button
            onClick={() => navigate('/routes')}
            className="bg-orange-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors"
          >
            Seleccionar ruta
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="relative w-full h-screen overflow-hidden bg-gray-100 flex flex-col">
      {/* Header */}
      <div className="bg-white shadow-sm p-4 z-10">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/routes')}
            className="text-gray-600 hover:text-gray-800 text-xl"
          >
            ←
          </button>
          <img 
            src="/logo.png" 
            alt="Smartstreet Logo" 
            className="h-16 w-auto object-contain"
            onError={(e) => {
              e.target.style.display = 'none'
            }}
          />
          <h1 className="text-xl font-bold flex-1">Navegación en curso</h1>
        </div>
      </div>

      {/* Mapa con ruta */}
      <div className="flex-1 relative">
        <MapContainer showDirections={true}>
          {/* Panel de información de la ruta */}
          <div className="absolute top-4 left-4 right-4 z-20">
            <div className="bg-white/95 backdrop-blur-sm rounded-lg p-4 shadow-lg">
              <h2 className="font-bold text-lg mb-2">{selectedRoute.name}</h2>
              <div className="flex items-center gap-4 text-sm text-gray-600">
                <span>⏱️ {selectedRoute.durationText}</span>
                <span>📏 {selectedRoute.distanceText}</span>
                <span>🛡️ {selectedRoute.securityLevel}</span>
              </div>
            </div>
          </div>

          {/* Instrucciones de navegación */}
          <NavigationInstructions route={selectedRoute} />
        </MapContainer>
      </div>
    </div>
  )
}

export default NavigationPage

