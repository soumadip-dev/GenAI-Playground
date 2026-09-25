import { NextResponse } from 'next/server';

const backendBaseUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? 'http://localhost:8080';

export async function POST() {
  try {
    const backendResponse = await fetch(`${backendBaseUrl}/api/knowledge-base/reset`, {
      method: 'POST',
    });

    const responseData = await backendResponse.json();

    return NextResponse.json(responseData, {
      status: backendResponse.status,
    });
  } catch (error) {
    console.error('API /knowledge-base/reset error:', error);

    return NextResponse.json(
      {
        success: false,
        error: 'Failed to communicate with the backend',
      },
      { status: 500 }
    );
  }
}
