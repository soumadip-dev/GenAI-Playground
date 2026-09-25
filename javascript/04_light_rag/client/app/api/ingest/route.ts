import { NextResponse } from 'next/server';

const backendBaseUrl = process.env.BACKEND_URL ?? 'http://localhost:8080';

export async function POST(request: Request) {
  try {
    const requestBody = await request.json();

    const backendResponse = await fetch(`${backendBaseUrl}/api/knowledge-base/ingest`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
      cache: 'no-store',
    });

    const responseData = await backendResponse.json();

    return NextResponse.json(responseData, {
      status: backendResponse.status,
    });
  } catch (error) {
    console.error('API /knowledge-base/ingest error:', error); // now actually shows the real cause, e.g. ECONNREFUSED

    return NextResponse.json(
      {
        success: false,
        error: 'Failed to communicate with the backend',
      },
      { status: 500 }
    );
  }
}
