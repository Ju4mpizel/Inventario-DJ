import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestInventario(unittest.TestCase):
    
    def setUp(self):
        # Creamos un navegador simulado para entrar a nuestra app
        self.navegador = app.test_client()

    #READ
    @patch("app.conectar")
    def test_index(self, conectar_falso):
        cursor_falso = MagicMock()
        conectar_falso.return_value.cursor.return_value = cursor_falso
        
        #Entramos a la página principal
        respuesta = self.navegador.get('/')
        
        #Si todo está bien, nos da 200 (OK)
        self.assertEqual(respuesta.status_code, 200)
        #Verificamos que se intentó hacer una consulta a la BD
        self.assertTrue(cursor_falso.execute.called)

    #CREATE
    @patch("app.conectar")
    def test_vista_agregar(self, conectar_falso):
        cursor_falso = MagicMock()
        conectar_falso.return_value.cursor.return_value = cursor_falso
        
        respuesta = self.navegador.get('/agregar')
        self.assertEqual(respuesta.status_code, 200)

    @patch("app.conectar")
    def test_guardar_polera(self, conectar_falso):
        bd_falsa = MagicMock()
        cursor_falso = MagicMock()
        conectar_falso.return_value = bd_falsa
        bd_falsa.cursor.return_value = cursor_falso
        
        
        datos = {'txtDescripcion': 'Test', 'txtTalla': 'S', 'txtPrecio': '10', 'txtStock': '5', 'txtMarca': '1'}
        respuesta = self.navegador.post('/guardar_polera', data=datos)
        
        self.assertEqual(respuesta.status_code, 302)
        bd_falsa.commit.assert_called_once()

    #DELETE
    @patch("app.conectar")
    def test_eliminar(self, conectar_falso):
        bd_falsa = MagicMock()
        cursor_falso = MagicMock()
        conectar_falso.return_value = bd_falsa
        bd_falsa.cursor.return_value = cursor_falso
        
        datos = {'txtID': '1'}
        respuesta = self.navegador.post('/ejecutar_eliminar', data=datos)
        
        self.assertEqual(respuesta.status_code, 302)
        bd_falsa.commit.assert_called_once()

    #UPDATE
    @patch("app.conectar")
    def test_actualizar(self, conectar_falso):
        bd_falsa = MagicMock()
        cursor_falso = MagicMock()
        conectar_falso.return_value = bd_falsa
        bd_falsa.cursor.return_value = cursor_falso
        
        datos = {'txtID': '1', 'txtDescripcion': 'Mod', 'txtTalla': 'M', 'txtPrecio': '20', 'txtStock': '2', 'txtMarca': '1'}
        respuesta = self.navegador.post('/ejecutar_actualizar', data=datos)
        
        self.assertEqual(respuesta.status_code, 302)
        bd_falsa.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()