package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"strings"
	"text/tabwriter"
)

func main() {
	cmd := exec.Command("kubectl", "get", "pods", "--all-namespaces")
	output, err := cmd.CombinedOutput()
	if err != nil {
		log.Fatalf("kubectl command failed: %v", err)
	}

	podStatusMap := parseKubectlOutput(string(output))

	w := tabwriter.NewWriter(os.Stdout, 0, 8, 2, ' ', 0)
	fmt.Fprintln(w, "NAME\tSTATUS")
	fmt.Fprintln(w, "--------\t------")

	podCheckResult := 0
	for pod, isRunning := range podStatusMap {
		status := "Running 1/1"
		if !isRunning {
			status = "Not Running"
			podCheckResult = 1
		}
		fmt.Fprintf(w, "%s\t%s\n", pod, status)
	}

	w.Flush()
	os.Exit(podCheckResult)
}

func parseKubectlOutput(output string) map[string]bool {
	result := make(map[string]bool)
	lines := strings.Split(output, "\n")

	for _, line := range lines {
		fields := strings.Fields(line)
		if len(fields) < 4 || fields[0] == "NAMESPACE" {
			continue
		}

		if fields[3] == "Running" && fields[2] == "1/1" {
			result[fields[1]] = true
		} else {
			result[fields[1]] = false
		}
	}
	return result
}
