import { Injectable } from '@angular/core';
import { DropdownQuestion } from './model/question-dropdown';
import { TextboxQuestion } from './model/question-textbox';
import { Monitoring } from './model/monitoring';
import { IsEqualConditional } from './conditionals/conditional-is-equal';


@Injectable()
export class MonitoringService {
    getMonitoring(id:number):Promise<Monitoring> {
        let name = 'Monitoring spółek komunalnych';
        let description = `Lorem ipsum dolor sit amet, consectetur adipisicing elit. Harum atque necessitatibus odio, quos ipsum numquam
 ipsam minus accusantium animi alias?`;
        let q1 = new TextboxQuestion(
            {
                id: 1,
                name: 'Czy to jest bardzo ważne?',
                description: 'Czy to jest bardzo ważne?',
                // hideConditions: []
            }
        );

        let q2 = new TextboxQuestion(
            {
                id: 2,
                name: 'Czy to jest bardzo ważne?',
                description: 'Czy to jest bardzo ważne?',
                // hideConditions: []
            }
        );

        let q3 = new DropdownQuestion(
            {
                id: 3,
                name: 'Jak bardzo jest to ważne?',
                description: 'Czy to jest bardzo ważne?',
                options: [
                    { key: '1', value: 'Bardzo ważne' },
                    { key: '2', value: 'Ważne' },
                    { key: '3', value: 'Średnio' },
                    { key: '4', value: 'Nie ważne' },
                    { key: '5', value: 'Nie istotne' },
                ],
                hideConditions: [
                    new IsEqualConditional({ target: q2, value: 'TAK' })
                ]
            }
        );

        let q4 = new DropdownQuestion(
             {
                id: 4,
                name: 'Jak bardzo jest to ważne?',
                description: 'Czy to jest bardzo ważne?',
                options: [
                       { key: '1', value: 'Bardzo ważne' },
                       { key: '2', value: 'Ważne' },
                       { key: '3', value: 'Średnio' },
                       { key: '4', value: 'Nie ważne' },
                       { key: '5', value: 'Nie istotne' },
                ],
                hideConditions: [
                       new IsEqualConditional({ target: q1, value: 'TAK' })
                ]
             }
        );

        let q5 = new DropdownQuestion(
            {
                id: 5,
                name: 'Czy ta informacja została opublikowana?',
                description: `Publikowanie informacji jest bardzo ważne. Lorem ipsum dolor
                sit amet, consectetur adipisicing elit. Incidunt, odio, error.
                Accusantium aspernatur architecto, similique nemo? Illo,
                neque alias consectetur?`,
                options: [
                    { key: '1', value: 'TAK' },
                    { key: '2', value: 'NIE' },
                ],
                hideConditions: [
                ]
            }
        );

        let q6 = new TextboxQuestion(
            {
                id: 6,
                name: 'Od kiedy ta informacja jest widoczna?',
                description: `Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatum similique adipisci eveniet deleniti non
 ad, eaque quae architecto numquam reprehenderit. Repudiandae molestias tempore dolores nihil provident sequi iste atque, explicabo.`,
                hideConditions: [
                       new IsEqualConditional({ target: q5, value: '2' }),
                       new IsEqualConditional({ target: q5, value: null })
                ]
            }
        );

        let questions = [q1, q2, q3, q4, q5, q6];

        let monitoring = new Monitoring({
            name,
            description,
            questions
        });

        return Promise.resolve(monitoring);
    }
}
