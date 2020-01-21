import { Component, OnInit } from '@angular/core';
import { InfoService } from '../services/info.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-viewer',
  templateUrl: './viewer.component.html',
  styleUrls: ['./viewer.component.css']
})
export class ViewerComponent implements OnInit {

  videoURL = {};
  keywords: Array<string> = ['Domain', 'Kingdom', 'Phylum', 'Class', 'Order'];
  times: number[][] = [[12, 13, 100], [21, 22, 23], [31, 32, 33]];

  constructor(private infoService: InfoService) {

    const link = this.infoService.getLink();
    console.log(link);

    if (link.substring(0, 24) === "https://www.youtube.com/"){
      this.videoURL = "https://qa-classifier.s3.amazonaws.com/Basic+Derivative+Rules.mp4";
    } else {
      this.videoURL = link;
    }
  }

  ngOnInit() {
  }


  jumpTo10sec() {
    const video = <HTMLMediaElement>document.getElementById('video1');
    video.currentTime = 10;
  }

  /** the parameter time is the seconds of the timeframe*/
  jumpTo(time) {
    const video = <HTMLMediaElement>document.getElementById('video1');
    video.currentTime = time;
  }

  getKeyword(num) {
    return this.keywords[num];
  }

  /** keywordNum mean which keyword and timeNum means the # of its timeframes*/
  getKeywordTime(keywordNum, timeNum) {
    // keywordNum -= 1;
    // timeNum -=1;
    return this.times[keywordNum - 1][timeNum - 1];
  }

  /** After getting the seconds in times 2D array, we are showing it on
   * the HTML page in the format of 00:00:00*/
  convertSecToTime(num) {
    let hour = num / 3600;
    hour = Math.floor(hour);
    //using Math library to make it whole number

    let minute = (num / 60) % 60;
    minute = Math.floor(minute);
    // console.log("minute is" + minute)

    let second = num % 60;
    second = Math.floor(second);

    return hour + ':' + minute + ':' + second;
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
