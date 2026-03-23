import json
import time
import random

from memory_profiler import profile
from ll import Node, DoublyLinkedList


class Song:
    def __init__(self, title: str, artist: str, album: str):
        self.title = title
        self.artist = artist
        self.album = album

    def __repr__(self):
        return f'"{self.title}" - {self.artist} [{self.album}]'


class Playlist:
    def __init__(self, name: str = "Mi Playlist"):
        self.name = name
        self._list = DoublyLinkedList()
        self._current = None
        self._shuffle = False
        self._shuffle_order = []
        self._shuffle_index = 0

    @profile
    def cargar_canciones(self, filepath: str):
        """Carga canciones dinámicamente desde un archivo JSON."""
        with open(filepath, "r", encoding="utf-8") as f:
            datos = json.load(f)

        for entrada in datos:
            cancion = Song(entrada["title"], entrada["artist"], entrada["album"])
            nodo = Node(cancion)
            self._list.insert_at_end(nodo)

        self._current = self._list.start

    def play(self):
        print(f"Reproduciendo: {self._current.data}")

    def next(self):
        if self._shuffle:
            self._shuffle_index = (self._shuffle_index + 1) % len(self._shuffle_order)
            self._current = self._shuffle_order[self._shuffle_index]
        else:
            if self._current.next is not None:
                self._current = self._current.next
            else:
                self._current = self._list.start
        self.play()

    def previous(self):
        if self._shuffle:
            self._shuffle_index = (self._shuffle_index - 1) % len(self._shuffle_order)
            self._current = self._shuffle_order[self._shuffle_index]
        else:
            if self._current.prev is not None:
                self._current = self._current.prev
            else:
                self._current = self._list.end
        self.play()

    def toggle_shuffle(self):
        """Activa o desactiva el modo shuffle."""
        self._shuffle = not self._shuffle

        if self._shuffle:
            # Recorre la lista usando punteros next para recolectar nodos
            referencias = []
            cursor = self._list.start
            while cursor is not None:
                referencias.append(cursor)
                cursor = cursor.next

            random.shuffle(referencias)
            self._shuffle_order = referencias

            # Ubica la canción actual dentro del nuevo orden
            for i, nodo in enumerate(self._shuffle_order):
                if nodo is self._current:
                    self._shuffle_index = i
                    break

            print(f"Shuffle ACTIVADO  — {len(self._shuffle_order)} canciones mezcladas")
        else:
            self._shuffle_order = []
            self._shuffle_index = 0
            print("Shuffle DESACTIVADO — orden secuencial restaurado")


if __name__ == "__main__":
    playlist = Playlist("DSA Midterm Playlist")

    # Perfilación temporal
    inicio = time.perf_counter()
    playlist.cargar_canciones("songs.json")
    fin = time.perf_counter()

    print(f"\nTiempo de carga : {(fin - inicio) * 1000:.4f} ms")
    print(f"Canciones cargadas: {len(playlist._list)}\n")

    # Demo de controles
    playlist.play()
    playlist.next()
    playlist.next()
    playlist.previous()

    print()
    playlist.toggle_shuffle()
    playlist.next()
    playlist.next()
    playlist.toggle_shuffle()
    playlist.next()
