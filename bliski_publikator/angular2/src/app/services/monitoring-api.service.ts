import { Observable }     from 'rxjs/Observable';

import { DOCUMENT } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Injectable, Inject } from '@angular/core';

import { Monitoring } from '../model/monitoring';

import { QuestionBase } from '../model/question-base';
import { TextboxQuestion } from '../model/question-textbox';
import { DropdownQuestion } from '../model/question-dropdown';
import { LongTextQuestion } from '../model/question-longtext';

import { IsEqualConditional } from '../conditionals/conditional-is-equal';
import { IsNullConditional } from '../conditionals/conditional-is-null';
import { IsMoreConditional } from '../conditionals/conditional-is-more';
import { IsLessConditional } from '../conditionals/conditional-is-less';

import { IsEqualCountCondition } from '../count.conditions/is-equal.cconditions';


@Injectable()
export class MonitoringService {

    constructor(private _http: HttpClient, @Inject(DOCUMENT) private _doc: any) { }

    saveMonitoring(monitoring: Monitoring) {
        var data = monitoring.toPlainObject();
        return this._http.post<any>(this._doc.location.pathname, data);
    }

    getMonitoring(id: number):Observable<Monitoring> {
        return this._http.get<any>(`/monitorings/${id}/api`)
            .map(data => {
                let questions = this.parseQuestionsList(data.questions);
                this.addConditions(data.questions, questions);
                return new Monitoring(
                    {
                        name: data.name,
                        description: data.description,
                        questions: questions
                    }
                );
            })
    }

    parseQuestionsList(questions:any[]):QuestionBase<any>[] {
        // console.log('parseQuestionsList', questions);
        return questions.map(this.parseQuestion);
    }

    parseQuestion(question):QuestionBase<any> {
        // console.log('parseQuestion', question);
        switch(question.type) {
            case 'long_text':
                return new LongTextQuestion(question);
            case 'short_text':
                return new TextboxQuestion(question);
            case 'choice':
                return new DropdownQuestion(question);
        }
        throw new Error(`Unsupported controlType [${question.controlType}].`);
    }

    addHideConditions(data:any[], questions:QuestionBase<any>[]) {
        // data.forEach( (q, i) => {
        //         var question = questions.find(t => q.id == t.id );
        //     });
    }

    addConditions(data: any[], questions: QuestionBase<any>[]) {
        data.forEach( (q, i) => {
                var question = questions[i];
                question.hideConditions = (q.hideConditions || []).map(c => this.parseHideConditions(c, questions));
                question.countConditions = (q.countConditions || []).map(this.parseCountCondition);
            });
    }

    parseHideConditions(data, questions: QuestionBase<any>[]) {
        let target = questions[data.target];
        switch(data.type) {
            case 'is-equal': {
                let value = data.value;
                return new IsEqualConditional({ target, value });
            }
            case 'is-null': {
                return new IsNullConditional({ target });
            }
            case 'is-less': {
                let value = data.value;
                return new IsLessConditional({ target, value });
            }
            case 'is-more': {
                let value = data.value;
                return new IsMoreConditional({ target, value });
            }
            

        }
        throw new Error(`Unsupported hide conditions [${data.hideConditions}].`);
    }

    parseCountCondition(data) {
        switch(data.type) {
            case 'is-equal': {
                let value = data.value;
                let point = data.point;
                return new IsEqualCountCondition({ value, point });
            }
        }
        throw new Error(`Unsupported count conditions [${data}].`);
    }
}
