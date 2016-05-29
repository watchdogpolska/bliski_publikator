import { EventEmitter } from '@angular/core';

import { QuestionBase } from './question-base';

export class Monitoring{
    name: string;
    description: string;
    instruction: string;
    private _questions: QuestionBase<any>[];
    questions_changes = new EventEmitter();
    max_point: number;

    constructor(options: {
        name?: string,
        description?: string,
        instruction?: string,
        questions?: QuestionBase<any>[],
        max_point?: number
    } = {}) {
        this.name = options.name || '';
        this.description = options.description || '';
        this.instruction = options.instruction || '';
        this._questions = options.questions || [];
        this.max_point = options.max_point || 0;
    }

    toPlainObject() {
        let obj = {
            'name': this.name,
            'description': this.description,
            'instruction': this.instruction,
            'max_point': this.max_points,
            'questions': this._questions.map(t => t.toPlainObject(this.questions))
        };
        return obj;
    }

    get questions() {
        return this._questions;
    }

    get max_points(){
        return this._questions.reduce((prev, curr) => prev + curr.max_point_sum, 0);
    }

    set questions(questions:QuestionBase<any>[]) {
        this._questions = questions;
        this.questions_changes.emit(questions);
    }

}
