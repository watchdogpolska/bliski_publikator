import { Observable }     from 'rxjs/Observable';

import { Injectable } from 'angular2/core';
import { Http } from 'angular2/http';

import { BaseApiService } from './api.base.service';


export class AnswerService extends BaseApiService {

    constructor(http:Http){
        super(http);
    }

    saveAnswers(answers: { id: number, value: string }[]) {
        return this.simple_post('answer', answers);
    }
}
