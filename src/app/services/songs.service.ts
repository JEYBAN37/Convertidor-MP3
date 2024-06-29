import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface ConvertedFile {
  id: number;
  video_url: string;
  audio_file: string;
  cover_image: string;
}

@Injectable({
  providedIn: 'root'
})
export class SongsService {
  private apiUrl = 'https://r0wm6ss0-8000.use.devtunnels.ms/converter/convert/';  // URL de la API
  private baseMediaUrl = 'https://r0wm6ss0-8000.use.devtunnels.ms/';  // URL base para los archivos media 
  private http = inject(HttpClient);

  list(): Observable<ConvertedFile[]> {
    return this.http.get<ConvertedFile[]>(this.apiUrl).pipe(
      map(songs => songs.map(song => ({
        ...song,
        audio_file: this.baseMediaUrl + song.audio_file,
        cover_image: this.baseMediaUrl + song.cover_image
      })))
    );
  }

  add(song:any){
    console.log(song)
    return this.http.post('https://r0wm6ss0-8000.use.devtunnels.ms/converter/convert/',song);
  }

  delete(id:any){
    return this.http.delete('https://r0wm6ss0-8000.use.devtunnels.ms/converter/convert/'+ id + '/')   }


}
