import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Test } from '../models/Test'

@Injectable({
  providedIn: 'root'
})
export class FlaskapiService {

  constructor(private httpClient: HttpClient) { }

  public server:string = "http://127.0.0.1:5000/api/";

  public getVideos(): Observable<string[]> { // get tags for video from database
    return this.httpClient.get<string[]>(this.server + "videos");
  }

  public searchTags(tag: string) {  // search for videos in database via tag names
    console.log("sending: " + tag);

    let testObj: Test = { search: tag }
    return this.httpClient.post<any[]>(this.server + "tags", testObj);
  }

  public upload(video: File, videoTitle: string, videoCategory: string) {
    console.log("sending: " + video);
    console.log(videoCategory);
    
    const form = new FormData();
    form.append('video', video, video.name);
    form.append('title', videoTitle);
    form.append('category', videoCategory);
    return this.httpClient.post<string>(this.server + "upload", form);
  }

  public playVideo() {
    console.log("requesting link...");

    return this.httpClient.get<string>(this.server + "play");
  }
}
