import { Component, Input, OnInit } from 'angular2/core';

import { ACCORDION_DIRECTIVES, DROPDOWN_DIRECTIVES } from 'ng2-bootstrap/ng2-bootstrap'

import { Monitoring } from '../model/monitoring'
import { QuestionBase } from '../model/question-base'
import { DropdownQuestion } from '../model/question-dropdown'
import { TextboxQuestion } from '../model/question-textbox'
import { QuestionEditComponent } from './question-edit.component'
import { MonitoringService } from '../services/monitoring-api.service'

import {TinyMceComponent } from '../tinymce/tinymce.value-accessor';

@Component({
    selector: 'sowp-question-editor',
    template: require('./question-editor.component.html'),
    directives: [
        QuestionEditComponent,
        ACCORDION_DIRECTIVES,
        DROPDOWN_DIRECTIVES,
        TinyMceComponent
    ],
    providers: [
        MonitoringService
    ]
    // viewProviders: [DragulaService],
})
export class QuestionEditorComponent implements OnInit {

    @Input()
    monitoring:Monitoring

    questions: QuestionBase<any>[]

    preview: Object;

    constructor(private _api:MonitoringService ){

    }
    ngOnInit() {
        this.questions = this.monitoring.questions;
        this.monitoring.questions_changes.subscribe(
            (questions) => this.questions = questions
        )
    }

    addDropdownQuestion() {
        this.monitoring.questions = [new DropdownQuestion(), ...this.questions];
    }

    addTextBoxQuestion(){
        this.monitoring.questions = [new TextboxQuestion(), ...this.questions];
    }

    removeQuestion(question: QuestionBase<any>){
        var index = this.questions.indexOf(question);
        if(index >= 0){
            this.monitoring.questions = [
                ...this.questions.slice(0, index),
                ...this.questions.slice(index + 1),
            ]
        }
    }

    moveQuestion(question: QuestionBase<any>, change: number, ev: MouseEvent){
        let index = this.questions.indexOf(question);
        let questions = this.questions.slice();
        questions[index] = questions[index + change];
        questions[index + change] = question;
        this.monitoring.questions = questions;
        ev.preventDefault();
    }

    saveMonitoring() {
        this._api.saveMonitoring(this.monitoring).subscribe(
            v => { console.log(v); alert("Zapisano"); },
            v => { console.log(v); alert("Błąd"); },
        );
    }
}
