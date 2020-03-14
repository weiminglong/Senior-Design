import { Component, OnInit } from '@angular/core';
import { InfoService } from '../services/info.service';

@Component({
  selector: 'app-viewer',
  templateUrl: './viewer.component.html',
  styleUrls: ['./viewer.component.css']
})
export class ViewerComponent implements OnInit {
  videoURL = {};
  timeFrames: string[][] = [];
  timeArray: string[] = [];
  link: string;
  title: string;

  constructor(private infoService: InfoService) {
    const link = this.infoService.getLink();
    this.title = this.infoService.getTitle();
    console.log("in viewer component:");
    console.log(link);
    console.log(this.title);

    if (link.toString().substring(0, 24) === "https://www.youtube.com/"){
      // CORS block does not allow playing youtube videos --> this is a least-effort temporary work around
      this.videoURL = "https://qa-classifier.s3.amazonaws.com/Basic+Derivative+Rules.mp4";
    } else {
      this.videoURL = link;
    }

    this.timeFrames = this.infoService.getTimeFrames();
    console.log("timeFrames:");
    console.log(this.timeFrames);
    // Capitalize first word
    for (let i in this.timeFrames){
      // console.log(this.timeFrames[i]);
      let word = this.timeFrames[i][0].charAt(0).toUpperCase() + this.timeFrames[i][0].substring(1);
      this.timeFrames[i][0] = word;
      //console.log(this.timeFrames[i]);
    }
  }

  ngOnInit() {
  }

  changeTime(time: string){
    console.log("value of time is:")
    console.log(time)

    const index = time.indexOf(":");

    const minutes = time.substring(0, index);
    const seconds = time.substring(index+1);
    console.log(time.indexOf(":"));
    console.log(time.substring(0, index));
    console.log(time.substring(index+1));

    let totalSec;
    let minToSec = (+minutes) * 60;
    let sec = +seconds;
    console.log("seconds:",sec)
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
