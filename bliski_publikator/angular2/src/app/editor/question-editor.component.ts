import { Component, Input, OnInit } from '@angular/core';

import { ACCORDION_DIRECTIVES, DROPDOWN_DIRECTIVES } from 'ng2-bootstrap/ng2-bootstrap'

import { Monitoring } from '../model/monitoring'
import { QuestionBase } from '../model/question-base'
import { DropdownQuestion, DropdownOption } from '../model/question-dropdown'
import { TextboxQuestion } from '../model/question-textbox'
import { QuestionEditComponent } from './question-edit.component'
import { MonitoringService } from '../services/monitoring-api.service'

import {TinyMceComponent } from '../tinymce/tinymce.value-accessor';

function isNotBlank(obj){
    return obj != null && typeof obj == "string" && obj.length > 0;
}

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
        this.monitoring.questions = [...this.questions, new DropdownQuestion()];
    }

    addTextBoxQuestion(){
        this.monitoring.questions = [...this.questions, new TextboxQuestion()];
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
        if(!this.validate()){
            return;
        }
        this._api.saveMonitoring(this.monitoring).subscribe(
            v => { document.location = v.url; },
            v => { console.log(v); alert("Błąd. Nie udało się zapisać. Sprawdź poprawność formularza."); },
        );
    }

    validate(){
        if (!isNotBlank(this.monitoring.name)){
            alert("Wypełnij pole `Tytuł`");
            return false;
        }
        if (!isNotBlank(this.monitoring.description)) {
            alert("Wypełnij pole `Opis`");
            return false;
        }

        let questions = this.monitoring.questions;
        if (questions.length == 0){
            alert("Dodaj przynajmniej jedno pytanie.");
            return false;
        }

        if (questions.every(t => !isNotBlank(t.name))) {
            alert("Upewnij się, że wszystkie pytania moja swoją etykietę.")
            return false;
        }

        let choice_question = <Array<DropdownQuestion>>questions.filter(t => t.controlType == 'choice');
        if (choice_question.length != 0) {
            if (choice_question.every(t => t.options.length < 2)){
                alert("Upewnij się, że wszystkie pytania wyboru mają dodane przynajmneij 2 opcje wyboru.")
                return false;
            }

            let options = <Array<DropdownOption>> Array.prototype.concat.apply([], choice_question.map(t => t.options));
            if (options.every(t => !isNotBlank(t.key)){
                alert("Upewnij się, że wszystkie odpowiedzi do pytań wielokrotnego wyboru mają swoje klucz.");
                return false;
            }

            if (options.every(t => !isNotBlank(t.value)){
                alert("Upewnij się, że wszystkie odpowiedzi do pytań wielokrotnego wyboru mają swoją wartość.");
                return false;
            }
            let question_key_list = choice_question.map(t => t.options.map(a => a.key));
            if (!question_key_list.every(a => a.every((b, bi, bc) => bc.indexOf(b) == bi)) ){
                alert("Wszystkie klucze w opcjach w pytaniach wyboru muszą być unikalne.");
                return false;
            }
        }

        return true;
    }
}
