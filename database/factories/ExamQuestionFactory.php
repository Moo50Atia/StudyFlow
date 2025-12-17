<?php

namespace Database\Factories;

use App\Models\Lecture;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\ExamQuestion>
 */
class ExamQuestionFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $ideas = [
            'This is a classic exam problem testing core concepts.',
            'Focus on the relationship between variables.',
            'Time management is key for this type of question.',
            'Read all options carefully before answering.',
            'Show all steps for full marks.',
            'This tests understanding of theoretical foundations.',
        ];

        return [
            'lecture_id' => Lecture::factory(),
            'question_image' => 'exam_questions/placeholder_exam_' . fake()->numberBetween(1, 10) . '.png',
            'idea' => fake()->randomElement($ideas),
            'solution_image' => 'exam_questions/placeholder_solution_' . fake()->numberBetween(1, 10) . '.png',
            'explanation' => fake()->paragraph(3),
            'dynamic_view_link' => 'https://docs.google.com/document/d/' . fake()->uuid() . '/edit',
        ];
    }
}
