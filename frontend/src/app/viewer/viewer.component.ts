import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-viewer',
  templateUrl: './viewer.component.html',
  styleUrls: ['./viewer.component.css']
})
export class ViewerComponent implements OnInit {


  videoURL = 'https://qa-classifier.s3.amazonaws.com/Taxonomy.mp4';

  constructor() { }

  ngOnInit() {
  }

  jumpTo10sec() {
    const video = document.getElementById('video1');
    video.currentTime = 10;
  }

    jumpTo(time) {
    const video = document.getElementById('video1');
    video.currentTime = time;
  }
}
