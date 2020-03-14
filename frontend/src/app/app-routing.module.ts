import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MainComponent } from './main/main.component';
import { UploadComponent } from './upload/upload.component';
import { ViewerComponent } from './viewer/viewer.component';
import { ListComponent } from './list/list.component';


const routes: Routes = [
  { path: "", component: MainComponent },
  { path: "upload", component: UploadComponent },
  { path: "list/viewer", component: ViewerComponent },
  { path: "list", component: ListComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
