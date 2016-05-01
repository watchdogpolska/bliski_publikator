import { EventEmitter } from 'angular2/core';

import { QuestionBase } from './question-base';

export class Monitoring{
    title: string;
    description: string;
    private _questions: QuestionBase<any>[];
    questions_changes = new EventEmitter();

    constructor(options: {
        title?: string,
        description?: string,
        questions?: QuestionBase<any>[]
    } = {}) {
        this.title = options.title || '';
        this.description = options.description || '';
        this._questions = options.questions || [];
    }

    toPlainObject() {
        let obj = {
            'title': this.title,
            'description': this.description,
            'questions': this._questions.map(t => t.toPlainObject())
        };
        return obj;
    }

    get questions() {
        return this._questions;
    }

    set questions(questions:QuestionBase<any>[]) {
        this._questions = questions;
        this.questions_changes.emit(questions);
    }

}
