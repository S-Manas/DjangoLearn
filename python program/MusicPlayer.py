#Note: made to run on windows machine

import os
from enum import Enum

class Genre(Enum):
    Pop = 0
    Jazz = 1
    Classic = 2

class Track:
    def __init__(self, name, location):
        self.name = name
        self.location = location

class Album:
    def __init__(self, artist_name, album_name, genre):
        self.artist_name = artist_name
        self.album_name = album_name
        self.genre = Genre(genre)
        self.tracks = []

albums = []

def print_album(album):
    print(f"Artist: {album.artist_name}")
    print(f"Album: {album.album_name}")
    print(f"Genre: {album.genre.name}")
    print("Tracks:")
    for track in album.tracks:
        print(f" - {track.name}")
        print(f" - {track.location}")

def print_all_albums():
    if not albums:
        print("No albums added yet.")
        return
    for album in albums:
        print_album(album)
        print()

def save_albums_to_file(filename):
    with open(filename, 'w') as file:
        file.write(f"{len(albums)}\n")
        for album in albums:
            file.write(f"{album.artist_name}\n")
            file.write(f"{album.album_name}\n")
            file.write(f"{album.genre.value}\n")
            file.write(f"{len(album.tracks)}\n")
            for track in album.tracks:
                file.write(f"{track.name}\n")
                file.write(f"{track.location}\n")

def load_albums_from_file(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} does not exist.")
        return
    with open(filename, 'r') as file:
        total_albums = int(file.readline().strip())
        global albums
        albums = []
        for _ in range(total_albums):
            artist_name = file.readline().strip()
            album_name = file.readline().strip()
            genre = int(file.readline().strip())
            num_tracks = int(file.readline().strip())
            new_album = Album(artist_name, album_name, genre)
            for _ in range(num_tracks):
                track_name = file.readline().strip()
                track_location = file.readline().strip()
                new_album.tracks.append(Track(track_name, track_location))
            albums.append(new_album)

def print_albums_by_genre():
    genre_choice = int(input("Enter genre to filter (0 - Pop, 1 - Jazz, 2 - Classic): "))
    genre = Genre(genre_choice)
    print(f"Albums of genre {genre.name}:")
    found = False
    for album in albums:
        if album.genre == genre:
            print_album(album)
            print()
            found = True
    if not found:
        print("No albums found for this genre.")

def play_track(track):
    print(f"Now playing: {track.name}")
    fullPath = track.location
    os.system(f'start "" "{fullPath}"')

def select_track_to_play():
    if not albums:
        print("No albums added yet.")
        return

    print("Select an album number to play:")
    for i, album in enumerate(albums):
        print(f"{i + 1}. {album.album_name}")

    album_choice = int(input()) - 1
    if album_choice < 0 or album_choice >= len(albums):
        print("Invalid album choice.")
        return

    selected_album = albums[album_choice]

    print(f"Select a track number to play from {selected_album.album_name}:")
    for i, track in enumerate(selected_album.tracks):
        print(f"{i + 1}. {track.name}")

    track_choice = int(input()) - 1
    if track_choice < 0 or track_choice >= len(selected_album.tracks):
        print("Invalid track choice.")
        return

    play_track(selected_album.tracks[track_choice])

def update_album():
    if not albums:
        print("No albums added yet.")
        return

    print("Select an album number to update:")
    for i, album in enumerate(albums):
        print(f"{i + 1}. {album.album_name}")

    album_choice = int(input()) - 1
    if album_choice < 0 or album_choice >= len(albums):
        print("Invalid album choice.")
        return

    selected_album = albums[album_choice]

    selected_album.album_name = input("Enter new album title: ")
    genre_choice = int(input("Enter new genre (0 - Pop, 1 - Jazz, 2 - Classic): "))
    selected_album.genre = Genre(genre_choice)
    save_albums_to_file("albums.txt")

def main():
    exit_program = False
    albumpath = ""

    while not exit_program:
        print("Main Menu:")
        print("1. Read in Albums")
        print("2. Display Albums")
        print("3. Select an Album to play")
        print("4. Update an existing Album")
        print("5. Exit the application")
        main_choice = int(input("Please enter your choice: "))

        if main_choice == 1:
            albumpath = input("Enter the filepath: ")
            load_albums_from_file(albumpath)
        elif main_choice == 2:
            display_choice = 0
            while display_choice != 3:
                print("Display Album Menu:")
                print("1. Display all Albums")
                print("2. Display Albums by Genre")
                print("3. Back to Main Menu")
                display_choice = int(input("Please enter your choice: "))
                
                if display_choice == 1:
                    print_all_albums()
                elif display_choice == 2:
                    print_albums_by_genre()
                elif display_choice == 3:
                    break
                else:
                    print("Invalid choice.")
        elif main_choice == 3:
            select_track_to_play()
        elif main_choice == 4:
            update_album()
        elif main_choice == 5:
            exit_program = True
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
