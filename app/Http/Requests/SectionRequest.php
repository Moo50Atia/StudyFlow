<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class SectionRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'lecture_id' => 'required|exists:lectures,id',
            'title' => 'required|string|max:255',
            'quick_summary' => 'nullable|string',
            'notebook_link' => 'nullable|url|max:500',
            'dynamic_view_link' => 'nullable|url|max:500',
        ];
    }

    public function messages(): array
    {
        return [
            'lecture_id.required' => 'Please select a lecture.',
            'lecture_id.exists' => 'The selected lecture does not exist.',
            'title.required' => 'The section title is required.',
            'title.max' => 'The section title must not exceed 255 characters.',
            'notebook_link.url' => 'The notebook link must be a valid URL.',
            'dynamic_view_link.url' => 'The dynamic view link must be a valid URL.',
        ];
    }
}
