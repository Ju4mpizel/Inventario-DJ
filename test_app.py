import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestInventarioDJ(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # --- READ ---
    @patch("app.conectar")
    def test_index(self, mock_conectar):
        mock_cursor = MagicMock()
        mock_conectar.return_value.cursor.return_value = mock_cursor
        
        # Ejecutamos la ruta principal
        respuesta = self.app.get('/')
        
        self.assertEqual(respuesta.status_code, 200)
        # Verificamos que se ejecutó al menos una consulta
        self.assertTrue(mock_cursor.execute.called)

    # --- CREATE ---
    @patch("app.conectar")
    def test_vista_agregar(self, mock_conectar):
        mock_cursor = MagicMock()
        mock_conectar.return_value.cursor.return_value = mock_cursor
        
        respuesta = self.app.get('/agregar')
        self.assertEqual(respuesta.status_code, 200)

    @patch("app.conectar")
    def test_guardar_polera(self, mock_conectar):
        mock_conexion = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conexion
        mock_conexion.cursor.return_value = mock_cursor
        
        datos = {'txtDescripcion': 'Test', 'txtTalla': 'S', 'txtPrecio': '10', 'txtStock': '5', 'txtMarca': '1'}
        respuesta = self.app.post('/guardar_polera', data=datos)
        
        self.assertEqual(respuesta.status_code, 302) # Redirección
        mock_conexion.commit.assert_called_once()

    # --- DELETE ---
    @patch("app.conectar")
    def test_eliminar(self, mock_conectar):
        mock_conexion = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conexion
        mock_conexion.cursor.return_value = mock_cursor
        
        datos = {'txtID': '1'}
        respuesta = self.app.post('/ejecutar_eliminar', data=datos)
        
        self.assertEqual(respuesta.status_code, 302)
        mock_conexion.commit.assert_called_once()

    # --- UPDATE ---
    @patch("app.conectar")
    def test_actualizar(self, mock_conectar):
        mock_conexion = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conexion
        mock_conexion.cursor.return_value = mock_cursor
        
        datos = {'txtID': '1', 'txtDescripcion': 'Mod', 'txtTalla': 'M', 'txtPrecio': '20', 'txtStock': '2', 'txtMarca': '1'}
        respuesta = self.app.post('/ejecutar_actualizar', data=datos)
        
        self.assertEqual(respuesta.status_code, 302)
        mock_conexion.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()