import { Injectable } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { QuestionBase } from '../model/question-base';

@Injectable()
export class QuestionControlService {

    constructor(private _fb: FormBuilder) {

    }

    toControlGroup(questions:QuestionBase<any>[]): FormGroup {
        let group = {};

        questions.forEach(t => group[t.key] = []);

        console.log(group);

        return this._fb.group(group);
    }
}
