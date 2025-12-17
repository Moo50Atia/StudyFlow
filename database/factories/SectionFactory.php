<?php

namespace Database\Factories;

use App\Models\Lecture;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Section>
 */
class SectionFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $sectionTitles = [
            'Key Definitions',
            'Core Concepts',
            'Step-by-Step Guide',
            'Examples and Exercises',
            'Summary Points',
            'Quick Review',
            'Important Formulas',
            'Practice Problems',
        ];

        return [
            'lecture_id' => Lecture::factory(),
            'title' => fake()->randomElement($sectionTitles),
            'quick_summary' => fake()->paragraph(2),
            'notebook_link' => 'https://notebooklm.google.com/notebook/' . fake()->uuid(),
            'dynamic_view_link' => 'https://docs.google.com/document/d/' . fake()->uuid() . '/edit',
        ];
    }
}
