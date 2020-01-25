import { Component, OnInit } from '@angular/core';
import { InfoService } from '../services/info.service';
import { Subscription } from 'rxjs';
import { stringify } from 'querystring';

@Component({
  selector: 'app-viewer',
  templateUrl: './viewer.component.html',
  styleUrls: ['./viewer.component.css']
})
export class ViewerComponent implements OnInit {

  videoURL = {};
  timeFrames: string[][] = [];
  keywords: Array<string> = ['Domain', 'Kingdom', 'Phylum', 'Class', 'Order'];
  times: number[][] = [[12, 13, 100], [21, 22, 23], [31, 32, 33]];
  link : string ;

  constructor(private infoService: InfoService) {

    //link ;

    const link = this.infoService.getLink();
    //link = this.infoService.getLink();
    
    console.log(link);

    if (link.toString().substring(0, 24) === "https://www.youtube.com/"){
      // CORS block does not allow playing youtube videos --> this is a least-effort temporary work around
      this.videoURL = "https://qa-classifier.s3.amazonaws.com/Basic+Derivative+Rules.mp4";
    } else {
      this.videoURL = link;
    }

    this.timeFrames = this.infoService.getTimeFrames();
    // Capitalize first word
    for (let i in this.timeFrames){
      // console.log(this.timeFrames[i]);
      let word = this.timeFrames[i][0].charAt(0).toUpperCase() + this.timeFrames[i][0].substring(1);
      this.timeFrames[i][0] = word;
      // console.log(this.timeFrames[i]);
    }
    //console.log(this.timeFrames);
  }

  ngOnInit() {
  }

  changeTime(time: string){
    let totalSec;
    let minToSec = (+time.charAt(0)) * 60;
    let sec = +time.substring(2);
    totalSec = minToSec + sec;

    (<HTMLMediaElement>document.getElementById('video1')).currentTime = totalSec;
  
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
}
