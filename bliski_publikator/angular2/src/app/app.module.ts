import { NgModule, Input }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule }   from '@angular/forms';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';

import { BsDropdownModule } from 'ngx-bootstrap';
import { AccordionModule } from 'ngx-bootstrap';
import { DragulaModule } from 'ng2-dragula';
import { TinymceModule } from 'angular2-tinymce';

import { AppComponent }  from './app.component';
import { SolverModule } from './solver/solver.module';
import { EditorModule } from './editor/editor.module';

import { AnswerService }   from './services/answers.service';
import { QuestionControlService }   from './question-control-service';
import { MonitoringService } from './services/monitoring-api.service'

@NgModule({
  imports: [
    BrowserModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken',
    }),
    BsDropdownModule.forRoot(),
    AccordionModule.forRoot(),
    EditorModule,
    SolverModule
  ],
  providers: [
    MonitoringService,
    AnswerService,
    QuestionControlService
  ],
  declarations: [
    AppComponent,
  ],
  bootstrap:    [
    AppComponent
  ]
})
export class AppModule { }
