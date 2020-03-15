import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { FlaskapiService } from '../services/flaskapi.service';
import { MatDialog } from '@angular/material';
import { UploadDialogComponent } from '../upload-dialog/upload-dialog.component';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {

  videoToUpload: File = null;
  categories: String[] = ["Math", "Physics", "Computer Science", "English", "History"];
  selectedVideo: string = "";
  isChecked: boolean = false;

  videoFile = new FormControl('', Validators.required);
  videoTitle = new FormControl('', Validators.required);
  videoSubject = new FormControl('', Validators.required);
  newSubject = new FormControl('', Validators.required);

  constructor(private flaskService: FlaskapiService,
    private dialog: MatDialog) { }

  ngOnInit() {
  }

  onVideoSelect(files: FileList){

    if (files.item(0) != null){
      this.videoToUpload = files.item(0);
      this.selectedVideo = files.item(0).name;
    } else {
      this.selectedVideo = "";
    }
  }

  onUpload(){
    // upload video...
    console.log("uploading: ");
    console.log(this.videoToUpload);
    console.log(this.videoTitle.value);

    let category;

    if (this.newSubject.value === ""){
      console.log(this.videoSubject.value);
      category = this.videoSubject.value;
    } else {
      console.log(this.newSubject.value);
      category = this.newSubject.value;
    }

    this.flaskService.upload(this.videoToUpload, this.videoTitle.value, category).subscribe(
      resp => {
        console.log(resp); // print
      },
      err => {
        console.log("something went wrong:" + err);
      }
    )

    this.dialog.open(UploadDialogComponent, {
      data: {
        message: "Your video will be uploaded shortly. Please check back later!"
      }
    });

  }

  resetForms(){
    this.videoSubject.reset();
    this.newSubject.reset();
  }

}
