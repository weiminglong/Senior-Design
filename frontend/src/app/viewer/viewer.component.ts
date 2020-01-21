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

  getKeyword1() {
    return "Keyword1 test";
  }

  getKeyword2() {
    return "Keyword2 test";
  }

  getKeyword3() {
    return "Keyword3 test";
  }

  getKeyword4() {
    return "Keyword4 test";
  }
  getKeyword5() {
    return "Keyword5 test";
  }
}
