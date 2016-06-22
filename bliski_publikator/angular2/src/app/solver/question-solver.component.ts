import {
    Component,
    Input,
    OnInit
} from '@angular/core';
import {
    FormBuilder,
    ControlGroup
} from '@angular/common';
import { Monitoring } from '../model/monitoring';
import { QuestionBase } from '../model/question-base';
import { QuestionControlService } from './question-control.service';
import { QuestionSolveItemComponent } from './question-solve-item.component';
import { AnswerService } from '../services/answers-api.service';

@Component({
    selector: 'sowp-question-solver',
    template: require('./question-solver.component.html'),
    providers: [
        QuestionControlService,
        AnswerService
    ],
    directives: [
        QuestionSolveItemComponent,
    ]
})
export class QuestionSolverComponent implements OnInit {
    @Input()
    monitoring: Monitoring;

    form: ControlGroup;
    visibility: { key:string, hidden:boolean }[] = [];


    constructor(private _fb: FormBuilder, private _api: AnswerService) {
        console.log(this._fb);
    }

    ngOnInit() {
        this.buildForm();
        console.log(this.form);
        this.form.valueChanges.subscribe((v) => this.validateVisibility(v));
        this.validateVisibility(this.form.value);
    }

    onSubmit() {
        let values = this.form.value;
        if(!this.validateAnswer(values)) {
            alert('Sprawdz poprawność wypełnienia formularza');
            return;
        };
        this._api
            .saveAnswers(this.generateAnswerSheet(values))
            .subscribe(
                data => { console.log(data); document.location = data.return_url; },
                error => { console.log('FAIL', error); }
            );
    }

    validateVisibility(values) {
        let questions = this.monitoring.questions;
        let visibility = [];
        questions.forEach(q => visibility.push({ key: q.key, hidden: q.isHidden(values) }) );
        this.visibility = visibility;
    }

     buildForm() {
        let group = {};
        this.monitoring.questions.forEach(t => group[t.key] = []);
        this.form = this._fb.group(group);
    }

    validateAnswer(values) {
        let questions = this.monitoring.questions;

        let list = Object.getOwnPropertyNames(values)
            .map(key => {
                return {
                    key: key,
                    value: values[key],
                    question: questions.find(q => q.key == key)
                };
            });
        let visible_list = list.filter(t => !t.question.isHidden(values));
        return visible_list.every(t => t.value != null)
            && visible_list.filter(t => typeof t == 'string').every(t => t.value.length > 0);
    }

    generateAnswerSheet(values) {
        console.log({ values });
        let questions = this.monitoring.questions;
        let answers = [];
        for (let answer_key in values) {
            let question = questions.find(q => q.key == answer_key);
            let curr_value = values[answer_key];
            answers.push({
                question_id: question.id,
                value: curr_value,
                point: question.calc_point_sum(curr_value);
            });
        }
        console.log(answers);
        return answers;
    }

    isHidden(question: QuestionBase<any>) {
        let o = this.visibility.find(t => t.key == question.key);
        if (!o) {
            return false;
        }
        return o.hidden;
    }
}
