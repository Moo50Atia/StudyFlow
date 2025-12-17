<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class LectureRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'subject_id' => 'required|exists:subjects,id',
            'title' => 'required|string|max:255',
            'pdf_path' => 'nullable|file|mimes:pdf|max:10240',
            'mindmap_path' => 'nullable|image|mimes:png|max:15360',
            'summary' => 'nullable|string',
        ];
    }

    public function messages(): array
    {
        return [
            'subject_id.required' => 'Please select a subject.',
            'subject_id.exists' => 'The selected subject does not exist.',
            'title.required' => 'The lecture title is required.',
            'title.max' => 'The lecture title must not exceed 255 characters.',
            'pdf_path.mimes' => 'The file must be a PDF document.',
            'pdf_path.max' => 'The PDF file must not exceed 10MB.',
            'mindmap_path.image' => 'The mind map must be an image file.',
            'mindmap_path.mimes' => 'The mind map must be a PNG image.',
            'mindmap_path.max' => 'The mind map file must not exceed 15MB.',
        ];
    }
}
