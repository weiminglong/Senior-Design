import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MainComponent } from './main/main.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { MaterialsModule } from './materials/materials.module';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { UploadComponent } from './upload/upload.component';
import { ViewerComponent } from './viewer/viewer.component';

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    ToolbarComponent,
    UploadComponent,
    ViewerComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialsModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
