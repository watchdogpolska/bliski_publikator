import { NgModule }            from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule }   from '@angular/forms';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';

import { BsDropdownModule } from 'ngx-bootstrap';
import { AccordionModule } from 'ngx-bootstrap';
import { DragulaModule } from 'ng2-dragula';
import { TinymceModule } from 'angular2-tinymce';

// import { TinyMceModule }   from '../tinymce/tinymce.module';

import { BasicInfoComponent } from './basic-info.component';
import { QuestionsComponent } from './questions.component';
import { QuestionComponent } from './question.component';
import { CountConditionsComponent } from './count-conditions.component';
import { EditorComponent } from './editor.component';
import { OptionsComponent } from './options.component'
import { QuestionConditionalsComponent } from './conditionals.component'


@NgModule({
    imports: [ 
        CommonModule,
        FormsModule,
        HttpClientModule,
        BsDropdownModule,
        AccordionModule,
        DragulaModule,
        TinymceModule.withConfig({
            skin_url: 'https://cdnjs.cloudflare.com/ajax/libs/tinymce/4.6.4/skins/lightgray'
        }),
    ],
    declarations: [
        BasicInfoComponent,
        EditorComponent,
        CountConditionsComponent,
        QuestionsComponent,
        QuestionComponent,
        OptionsComponent,
        QuestionConditionalsComponent
    ],
    exports: [
        EditorComponent
    ]
})
export class EditorModule { }