import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { BsDropdownModule } from 'ngx-bootstrap';
import { AccordionModule } from 'ngx-bootstrap';
import { DragulaModule } from 'ng2-dragula';

import { SolverComponent } from './solver.component';
import { SolveItemComponent } from './solve-item.component';

@NgModule({
    imports: [ 
        CommonModule,
        // FormsModule,
        ReactiveFormsModule,
        HttpClientModule,
    ],
    declarations: [
        SolverComponent,
        SolveItemComponent,
    ],
    exports: [
        SolverComponent,
    ]
})
export class SolverModule { }