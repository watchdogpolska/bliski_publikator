import { NgModule }            from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule }   from '@angular/forms';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';

import { BsDropdownModule } from 'ngx-bootstrap';
import { AccordionModule } from 'ngx-bootstrap';
import { DragulaModule } from 'ng2-dragula';
import { TinymceModule } from 'angular2-tinymce';

// import { TinyMceModule }   from '../tinymce/tinymce.module';

import { CountConditionEditComponent } from './count-condition-edit.component';
import { QuestionEditorComponent } from './question-editor.component';
import { QuestionEditComponent } from './question-edit.component';
import { QuestionOptionEditComponent } from './question-option-edit.component'
import { QuestionConditionalsComponent } from './question-conditionals.component'


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
        CountConditionEditComponent,
        QuestionEditorComponent,
        QuestionEditComponent,
        QuestionOptionEditComponent,
        QuestionConditionalsComponent
    ],
    exports: [
        QuestionEditorComponent
    ]
})
export class EditorModule { }