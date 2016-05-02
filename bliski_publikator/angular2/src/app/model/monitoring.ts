import { EventEmitter } from 'angular2/core';

import { QuestionBase } from './question-base';

export class Monitoring{
    name: string;
    description: string;
    private _questions: QuestionBase<any>[];
    questions_changes = new EventEmitter();

    constructor(options: {
        name?: string,
        description?: string,
        questions?: QuestionBase<any>[]
    } = {}) {
        this.name = options.name || '';
        this.description = options.description || '';
        this._questions = options.questions || [];
    }

    toPlainObject() {
        let obj = {
            'name': this.name,
            'description': this.description,
            'questions': this._questions.map(t => t.toPlainObject(this.questions))
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
