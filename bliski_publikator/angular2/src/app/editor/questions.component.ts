import { Component, Input } from '@angular/core';

import { DragulaService } from 'ng2-dragula/ng2-dragula';


import { Monitoring } from '../model/monitoring';
import { QuestionBase } from '../model/question-base';
import { DropdownQuestion, DropdownOption } from '../model/question-dropdown';
import { TextboxQuestion } from '../model/question-textbox';
import { LongTextQuestion } from '../model/question-longtext';

@Component({
    selector: 'sowp-questions',
    template: require('./questions.component.html'),
})
export class QuestionsComponent {
    @Input()
    monitoring: Monitoring;

    constructor( private _dragula: DragulaService) {
        this._dragula.setOptions('questions', {
            moves: function(el, container, handle:HTMLElement) {
                return handle.classList.contains('dragula-handle');
            }
        });
    }

    addDropdownQuestion() {
        this.monitoring.questions = [...this.monitoring.questions, new DropdownQuestion()];
    }

    addTextBoxQuestion() {
        this.monitoring.questions = [...this.monitoring.questions, new TextboxQuestion()];
    }

    addLongTextQuestion() {
        this.monitoring.questions = [...this.monitoring.questions, new LongTextQuestion()];
    }

    removeQuestion(question: QuestionBase<any>) {
        var index = this.monitoring.questions.indexOf(question);
        if(index >= 0) {
            this.monitoring.questions = [
                ...this.monitoring.questions.slice(0, index),
                ...this.monitoring.questions.slice(index + 1),
            ];
        }
    }

    moveQuestion(question: QuestionBase<any>, change: number, ev: MouseEvent) {
        let index = this.monitoring.questions.indexOf(question);
        let questions = this.monitoring.questions.slice();
        questions[index] = questions[index + change];
        questions[index + change] = question;
        this.monitoring.questions = questions;
        ev.preventDefault();
    }
}

