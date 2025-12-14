<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class BulkLectureRequest extends FormRequest
{
    public function authorize(): bool
    {
        return auth()->check() && auth()->user()->role === 'admin';
    }

    public function rules(): array
    {
        return [
            'lectures' => 'required|array|min:1',
            'lectures.*.title' => 'required|string|max:255',
            'lectures.*.summary' => 'nullable|string',
        ];
    }

    public function messages(): array
    {
        return [
            'lectures.required' => 'At least one lecture is required.',
            'lectures.*.title.required' => 'Each lecture must have a title.',
        ];
    }
}
