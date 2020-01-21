import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-viewer',
  templateUrl: './viewer.component.html',
  styleUrls: ['./viewer.component.css']
})
export class ViewerComponent implements OnInit {

  videoURL = 'https://qa-classifier.s3.amazonaws.com/Taxonomy.mp4';

  constructor() { }
  const keywords: Array<string> = ['Domain', 'Kingdom', 'Phylum', 'Class', 'Order'];
  const times: number[][] = [[12, 13, 100], [21, 22, 23], [31, 32, 33]];

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

  getKeyword(num) {
    return this.keywords[num];
  }

  
  getKeywordTime(keywordNum, timeNum) {

  }

  convertSecToTime(num) {
    let hour = num / 3600;
    hour = Math.floor(hour);

    let minute = (num / 60) % 60;
    minute = Math.floor(minute);
    // console.log("minute is" + minute)

    let second = num % 60;
    second = Math.floor(second);

    return hour + ":" + minute + ":" + second;
  }
  // getKeyword1() {
  //   return "Keyword1 test";
  // }
  //
  // getKeyword2() {
  //   return "Keyword2 test";
  // }
  //
  // getKeyword3() {
  //   return "Keyword3 test";
  // }
  //
  // getKeyword4() {
  //   return "Keyword4 test";
  // }
  // getKeyword5() {
  //   return "Keyword5 test";
  // }
}
