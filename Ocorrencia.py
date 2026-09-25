import json

class Ocorrencia:
    def __init__(self, numero_bo, latitude, longitude, natureza):
        self._natureza_valida = self.naturezas_validas()
        self.numero_bo = numero_bo
        self.latitude = latitude
        self.longitude = longitude
        self.natureza = natureza

    @property
    def numero_bo(self):
        return self._numero_bo

    @numero_bo.setter
    def numero_bo(self, novo_numero):
        self._numero_bo = novo_numero

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, nova_latitude):
        if -90.0 < nova_latitude < 90.0:
            self._latitude = nova_latitude
        else:
            raise ValueError('latitude invalida!')

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, nova_longitude):
        if -180.0 < nova_longitude < 180.0:
            self._longitude = nova_longitude
        else:
            raise ValueError('longitude invalida!')

    @property
    def natureza(self):
        return self._natureza

    @natureza.setter
    def natureza(self, novo_tipo):
        if novo_tipo in self._natureza_valida:
            self._natureza = novo_tipo
        else:
            raise Exception('natureza invalida!')

    @staticmethod
    def naturezas_validas():
        with open('naturezas_permitidas.json', 'r', encoding='utf-8') as f:
            return set(json.load(f))