import requests
import unittest

class ApiTest(unittest.TestCase):

    url_read = 'http://127.0.0.1:8000/blog/read'
    url_read_one = 'http://127.0.0.1:8000/blog/read/'
    url_add = 'http://127.0.0.1:8000/blog/add/'
    url_del = 'http://127.0.0.1:8000/blog/del/'
    url_update = 'http://127.0.0.1:8000/blog/update/'

    Teste ={
        "id": 3,
        "Titulo": "Fabrica de Chocolate",
        "Autor": "Mario",
        "Conteudo": "Alguma coisa"
    }

    Teste_2 ={
        "id": 3,
        "Titulo": "Super Mario World",
        "Autor": "Mario",
        "Conteudo": "Alguma coisa"
    }

    Teste_3 ={
        "id": 2,
        "Titulo": "Super Mario World",
        "Autor": "Mario",
        "Conteudo": "Alguma coisa"
    }

    def test_get_all_posts(self):
        r = requests.get(ApiTest.url_read)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_add_post(self):
        # Verifica se o post foi adicionado
        c = requests.post(url= ApiTest.url_add, json=ApiTest.Teste)
        self.assertEqual(c.status_code, 200)
        # Verifica se o método add funciona como update, que não pode acontecer
        c = requests.post(url= ApiTest.url_add, json=ApiTest.Teste_2)
        self.assertEqual(c.status_code, 200)

    def test_get_one_post(self):
        r = requests.get(url= ApiTest.url_read_one + '%d' %
        (ApiTest.Teste.get('id')))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), ApiTest.Teste)

    def test_update_post(self):
        # Verifica a atualização de um post
        u = requests.put(url= ApiTest.url_update + '%d' % 
        (ApiTest.Teste_2.get('id')), json=ApiTest.Teste_2)
        self.assertEqual(u.status_code, 200)
        r = requests.get(url= ApiTest.url_read_one + '%d' %
        (ApiTest.Teste.get('id')))
        self.assertDictEqual(r.json(), ApiTest.Teste_2)
        # Verifica se o método update consegue adiciona novos post, que não pode acontecer
        u = requests.put(url= ApiTest.url_update + '%d' % 
        (ApiTest.Teste_3.get('id')), json=ApiTest.Teste_3)
        self.assertEqual(u.status_code, 200)
        r = requests.get(ApiTest.url_read)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)
    
    def test_del_pos(self):
        d = requests.delete(url= ApiTest.url_del + '%d' % 
        (ApiTest.Teste_2.get('id')))
        self.assertEqual(d.status_code, 200)
        r = requests.get(ApiTest.url_read)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(ApiTest("test_get_all_posts"))
    suite.addTest(ApiTest("test_add_post"))
    suite.addTest(ApiTest("test_get_one_post"))
    suite.addTest(ApiTest("test_update_post"))
    suite.addTest(ApiTest("test_del_pos"))
    runner = unittest.TextTestRunner()
    runner.run(suite)