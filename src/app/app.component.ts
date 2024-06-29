import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { SongsService } from './services/songs.service';

export interface song {
  id: number,
  video_url: string,
  audio_file: string,
  cover_image:string,
  video_title :string,
}


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports:[FormsModule],
  standalone: true,
})
export class AppComponent implements OnInit {
  currentAudio: HTMLAudioElement | undefined; // Mantén una referencia al audio actual
  favoriteFramework = '';
  songs: any = [];
  private songService = inject(SongsService)
  isPlaying = false; // Estado de reproducción actual

ngOnInit(): void {
this.songService.list().subscribe(songs =>{
  this.songs = songs 
})
}
  sendUrl() {
  const songItem = {
    url:this.favoriteFramework
  }
   this.songService.add(songItem).subscribe((response: any) => {
    alert(response.id); 
    window.location.reload(); // Recarga la página// Muestra mensaje del backend en alerta
  });

  }

  playAudio(audioUrl: string): void {
    if (this.currentAudio && this.isPlaying) {
      this.stopAudio(); // Si ya está reproduciendo, detener
    } else {
      this.currentAudio = new Audio(audioUrl);
      this.currentAudio.play();
      this.isPlaying = true; // Cambiar estado de reproducción
    }
  }

  stopAudio(): void {
    if (this.currentAudio) {
      this.currentAudio.pause(); // Pausar el audio
      this.currentAudio = undefined; // Limpiar referencia al audio actual
      this.isPlaying = false; // Cambiar estado de reproducción
    }
  }

  songDelete(id: string): void {
    this.songService.delete(id).subscribe(
      (response: any) => {
        alert('Canción eliminada correctamente');
        this.ngOnInit(); // Recargar la lista de canciones después de eliminar
      },
      (error) => {
        alert(error.error ? error.error.message : 'Error al eliminar la canción');
      }
    );
  }
  
}
