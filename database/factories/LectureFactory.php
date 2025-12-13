<?php

namespace Database\Factories;

use App\Models\Subject;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Lecture>
 */
class LectureFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $lectureTitles = [
            'Introduction to the Subject',
            'Fundamental Concepts',
            'Advanced Techniques',
            'Problem Solving Strategies',
            'Practical Applications',
            'Review and Summary',
            'Case Studies',
            'Laboratory Practice',
            'Theoretical Foundations',
            'Modern Approaches',
        ];

        return [
            'subject_id' => Subject::factory(),
            'title' => 'Lecture ' . fake()->numberBetween(1, 20) . ': ' . fake()->randomElement($lectureTitles),
            'pdf_path' => null,
            'summary' => fake()->paragraph(3),
        ];
    }
}
