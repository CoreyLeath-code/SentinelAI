package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestMuxExposesInstanceHeaderOnlyWhenEnabled(t *testing.T) {
	t.Setenv("EXPOSE_INSTANCE_ID", "true")
	t.Setenv("INSTANCE_ID", "test-replica")

	response := httptest.NewRecorder()
	newMux().ServeHTTP(response, httptest.NewRequest(http.MethodGet, "/health", nil))

	if response.Code != http.StatusOK {
		t.Fatalf("health status = %d, want %d", response.Code, http.StatusOK)
	}
	if got := response.Header().Get("X-Instance-ID"); got != "test-replica" {
		t.Fatalf("X-Instance-ID = %q, want test-replica", got)
	}
}

func TestMuxDoesNotExposeInstanceHeaderByDefault(t *testing.T) {
	t.Setenv("EXPOSE_INSTANCE_ID", "false")
	t.Setenv("INSTANCE_ID", "test-replica")

	response := httptest.NewRecorder()
	newMux().ServeHTTP(response, httptest.NewRequest(http.MethodGet, "/health", nil))

	if got := response.Header().Get("X-Instance-ID"); got != "" {
		t.Fatalf("X-Instance-ID = %q, want no header", got)
	}
}
