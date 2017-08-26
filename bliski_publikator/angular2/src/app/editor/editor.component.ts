import { Component, Input, OnInit } from '@angular/core';

import { MonitoringService } from '../services/monitoring-api.service';

import { Monitoring } from '../model/monitoring';
import { QuestionBase } from '../model/question-base';
import { DropdownQuestion, DropdownOption } from '../model/question-dropdown';

function isNotBlank(obj) {
    return obj != null && typeof obj == 'string' && obj.length > 0;
}

@Component({
    selector: 'sowp-editor',
    template: require('./editor.component.html'),
})
export class EditorComponent {

    @Input()
    monitoring: Monitoring;

    constructor(private _api: MonitoringService) {
    }

    saveMonitoring() {
        if(!this.validate()) {
            return;
        }
        this._api.saveMonitoring(this.monitoring).subscribe(
            v => { document.location.href = v.url; },
            v => { console.log(v); alert('Błąd. Nie udało się zapisać. Sprawdź poprawność formularza.'); },
        );
    }

    validate() {
        if (!isNotBlank(this.monitoring.name)) {
            alert('Wypełnij pole `Tytuł`');
            return false;
        }
        if (!isNotBlank(this.monitoring.description)) {
            alert('Wypełnij pole `Opis`');
            return false;
        }

        let questions = this.monitoring.questions;
        if (questions.length == 0) {
            alert('Dodaj przynajmniej jedno pytanie.');
            return false;
        }

        if (questions.every(t => !isNotBlank(t.name))) {
            alert('Upewnij się, że wszystkie pytania moja swoją etykietę.');
            return false;
        }

        let choice_question = <Array<DropdownQuestion>>questions.filter(t => t.controlType == 'choice');
        if (choice_question.length != 0) {
            if (choice_question.every(t => t.options.length < 2)) {
                alert('Upewnij się, że wszystkie pytania wyboru mają dodane przynajmneij 2 opcje wyboru.');
                return false;
            }

            let options = <Array<DropdownOption>> Array.prototype.concat.apply([], choice_question.map(t => t.options));
            if (options.every(t => !isNotBlank(t.key))) {
                alert('Upewnij się, że wszystkie odpowiedzi do pytań wielokrotnego wyboru mają swoje klucz.');
                return false;
            }

            if (options.every(t => !isNotBlank(t.value))) {
                alert('Upewnij się, że wszystkie odpowiedzi do pytań wielokrotnego wyboru mają swoją wartość.');
                return false;
            }
            let question_key_list = choice_question.map(t => t.options.map(a => a.key));
            if (!question_key_list.every(a => a.every((b, bi, bc) => bc.indexOf(b) == bi))) {
                alert('Wszystkie klucze w opcjach w pytaniach wyboru muszą być unikalne.');
                return false;
            }
        }

        return true;
    }
}
