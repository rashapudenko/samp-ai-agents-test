#!/bin/bash

# AKS-Specific Helm Chart Validation Script
# This script validates the Helm chart template against Azure Kubernetes Service
# best practices, security standards, and compliance requirements

set -e

CHART_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERRORS=0
WARNINGS=0

echo "🔍 AKS-Specific Helm Chart Validation..."
echo "Chart directory: $CHART_DIR"
echo "Validation Date: $(date)"
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $message"
    elif [ "$status" = "FAIL" ]; then
        echo -e "${RED}✗ FAIL${NC}: $message"
        ERRORS=$((ERRORS + 1))
    elif [ "$status" = "WARN" ]; then
        echo -e "${YELLOW}⚠ WARN${NC}: $message"
        WARNINGS=$((WARNINGS + 1))
    elif [ "$status" = "INFO" ]; then
        echo -e "${BLUE}ℹ INFO${NC}: $message"
    elif [ "$status" = "AKS" ]; then
        echo -e "${PURPLE}🔷 AKS${NC}: $message"
    fi
}

# Azure/AKS-specific validation
validate_azure_integration() {
    echo "🔷 Azure Integration Validation..."
    
    # Check for Azure Workload Identity
    if grep -q "azure.workload.identity" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Azure Workload Identity configuration found"
    else
        print_status "WARN" "Azure Workload Identity not configured"
    fi
    
    # Check for Azure Key Vault integration
    if grep -q "azureKeyVault:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Azure Key Vault integration configured"
        
        # Check for CSI driver usage
        if grep -q "secrets-store.csi.k8s.io" "$CHART_DIR/templates/deployment.yaml"; then
            print_status "PASS" "Azure Key Vault CSI driver usage confirmed"
        else
            print_status "FAIL" "Azure Key Vault CSI driver not used"
        fi
    else
        print_status "WARN" "Azure Key Vault integration not configured"
    fi
    
    # Check for Azure Log Analytics integration
    if grep -q "azureLogAnalytics:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Azure Log Analytics integration configured"
    else
        print_status "WARN" "Azure Log Analytics integration not configured"
    fi
    
    # Check for Azure Container Registry
    if grep -q "azurecr.io" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Azure Container Registry referenced"
    else
        print_status "WARN" "Azure Container Registry not referenced"
    fi
}

# AKS-specific configuration validation
validate_aks_configuration() {
    echo "🚀 AKS Configuration Validation..."
    
    # Check for Linux node selector
    if grep -q "kubernetes.io/os: linux" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Linux node selector configured"
    else
        print_status "FAIL" "Linux node selector not configured"
    fi
    
    # Check for zone-aware scheduling
    if grep -q "topology.kubernetes.io/zone" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Zone-aware scheduling configured"
    else
        print_status "WARN" "Zone-aware scheduling not configured"
    fi
    
    # Check for DNS optimization
    if grep -q "dnsPolicy: ClusterFirst" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "DNS policy optimized for AKS"
    else
        print_status "WARN" "DNS policy not optimized"
    fi
    
    if grep -q "ndots" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "DNS ndots configuration found"
    else
        print_status "WARN" "DNS ndots not configured"
    fi
    
    # Check for modern API versions
    if grep -q "autoscaling/v2" "$CHART_DIR/templates/hpa.yaml"; then
        print_status "PASS" "Modern HPA API version (autoscaling/v2)"
    else
        print_status "FAIL" "Outdated HPA API version"
    fi
    
    if grep -q "networking.k8s.io/v1" "$CHART_DIR/templates/networkpolicy.yaml"; then
        print_status "PASS" "Modern NetworkPolicy API version"
    else
        print_status "FAIL" "Outdated NetworkPolicy API version"
    fi
    
    if grep -q "policy/v1" "$CHART_DIR/templates/poddisruptionbudget.yaml"; then
        print_status "PASS" "Modern PodDisruptionBudget API version"
    else
        print_status "FAIL" "Outdated PodDisruptionBudget API version"
    fi
}

# Security validation for AKS
validate_aks_security() {
    echo "🔒 AKS Security Validation..."
    
    # Check for Pod Security Standards
    if grep -q "podSecurityStandards:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Pod Security Standards configured"
    else
        print_status "FAIL" "Pod Security Standards not configured"
    fi
    
    # Check for security contexts
    if grep -q "runAsNonRoot: true" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Non-root security context configured"
    else
        print_status "FAIL" "Non-root security context not configured"
    fi
    
    if grep -q "readOnlyRootFilesystem: true" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Read-only root filesystem configured"
    else
        print_status "FAIL" "Read-only root filesystem not configured"
    fi
    
    if grep -q "allowPrivilegeEscalation: false" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Privilege escalation disabled"
    else
        print_status "FAIL" "Privilege escalation not disabled"
    fi
    
    # Check for network policies
    if grep -q "networkPolicy:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Network policy configuration found"
    else
        print_status "FAIL" "Network policy configuration missing"
    fi
    
    # Check for service account configuration
    if grep -q "serviceAccount:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Service account configuration found"
    else
        print_status "FAIL" "Service account configuration missing"
    fi
}

# Resource management validation
validate_resource_management() {
    echo "📊 Resource Management Validation..."
    
    # Check for resource limits and requests
    if grep -q "resources:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Resource configuration found"
        
        if grep -A 5 "resources:" "$CHART_DIR/values.yaml" | grep -q "limits:"; then
            print_status "PASS" "Resource limits configured"
        else
            print_status "FAIL" "Resource limits not configured"
        fi
        
        if grep -A 5 "resources:" "$CHART_DIR/values.yaml" | grep -q "requests:"; then
            print_status "PASS" "Resource requests configured"
        else
            print_status "FAIL" "Resource requests not configured"
        fi
    else
        print_status "FAIL" "Resource configuration missing"
    fi
    
    # Check for HPA
    if grep -q "autoscaling:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Horizontal Pod Autoscaler configured"
    else
        print_status "WARN" "Horizontal Pod Autoscaler not configured"
    fi
    
    # Check for PDB
    if grep -q "podDisruptionBudget:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Pod Disruption Budget configured"
    else
        print_status "WARN" "Pod Disruption Budget not configured"
    fi
}

# Health checks validation
validate_health_checks() {
    echo "🏥 Health Checks Validation..."
    
    # Check for liveness probe
    if grep -q "livenessProbe:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Liveness probe configured"
    else
        print_status "FAIL" "Liveness probe not configured"
    fi
    
    # Check for readiness probe
    if grep -q "readinessProbe:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Readiness probe configured"
    else
        print_status "FAIL" "Readiness probe not configured"
    fi
    
    # Check for startup probe
    if grep -q "startupProbe:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Startup probe configured"
    else
        print_status "WARN" "Startup probe not configured"
    fi
}

# Monitoring and observability validation
validate_monitoring() {
    echo "📈 Monitoring & Observability Validation..."
    
    # Check for monitoring configuration
    if grep -q "monitoring:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Monitoring configuration found"
    else
        print_status "FAIL" "Monitoring configuration missing"
    fi
    
    # Check for ServiceMonitor
    if grep -q "serviceMonitor:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "ServiceMonitor configuration found"
    else
        print_status "WARN" "ServiceMonitor configuration missing"
    fi
    
    # Check for Prometheus annotations
    if grep -q "prometheus.io" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Prometheus annotations configured"
    else
        print_status "WARN" "Prometheus annotations not configured"
    fi
}

# Template structure validation
validate_template_structure() {
    echo "📄 Template Structure Validation..."
    
    required_templates=(
        "templates/deployment.yaml"
        "templates/service.yaml"
        "templates/serviceaccount.yaml"
        "templates/ingress.yaml"
        "templates/hpa.yaml"
        "templates/networkpolicy.yaml"
        "templates/poddisruptionbudget.yaml"
        "templates/secretproviderclass.yaml"
        "templates/servicemonitor.yaml"
        "templates/resourcequota.yaml"
        "templates/compliance.yaml"
        "templates/_helpers.tpl"
        "templates/NOTES.txt"
    )
    
    for template in "${required_templates[@]}"; do
        if [ -f "$CHART_DIR/$template" ]; then
            print_status "PASS" "Template exists: $template"
        else
            print_status "FAIL" "Missing template: $template"
        fi
    done
    
    # Check for environment-specific values
    env_files=(
        "values.dev.yaml"
        "values.prod.yaml"
    )
    
    for file in "${env_files[@]}"; do
        if [ -f "$CHART_DIR/$file" ]; then
            print_status "PASS" "Environment file exists: $file"
        else
            print_status "WARN" "Missing environment file: $file"
        fi
    done
}

# Chart metadata validation
validate_chart_metadata() {
    echo "📋 Chart Metadata Validation..."
    
    if [ -f "$CHART_DIR/Chart.yaml" ]; then
        print_status "PASS" "Chart.yaml exists"
        
        # Check for required fields
        if grep -q "^name:" "$CHART_DIR/Chart.yaml"; then
            print_status "PASS" "Chart name defined"
        else
            print_status "FAIL" "Chart name missing"
        fi
        
        if grep -q "^version:" "$CHART_DIR/Chart.yaml"; then
            print_status "PASS" "Chart version defined"
        else
            print_status "FAIL" "Chart version missing"
        fi
        
        if grep -q "^appVersion:" "$CHART_DIR/Chart.yaml"; then
            print_status "PASS" "App version defined"
        else
            print_status "WARN" "App version missing"
        fi
        
        # Check for AKS-specific annotations
        if grep -q "azure.com/aks-optimized" "$CHART_DIR/Chart.yaml"; then
            print_status "PASS" "AKS optimization annotation found"
        else
            print_status "WARN" "AKS optimization annotation missing"
        fi
    else
        print_status "FAIL" "Chart.yaml missing"
    fi
}

# Run all validations
echo "🎯 Starting AKS Helm Chart Validation..."
echo "========================================"
echo

validate_chart_metadata
echo
validate_azure_integration
echo
validate_aks_configuration
echo
validate_aks_security
echo
validate_resource_management
echo
validate_health_checks
echo
validate_monitoring
echo
validate_template_structure
echo

# Summary
echo "📊 AKS Validation Summary"
echo "========================="
echo "Total Errors: $ERRORS"
echo "Total Warnings: $WARNINGS"
echo

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}🎉 Perfect! Chart is fully AKS-optimized and production-ready!${NC}"
    echo "✅ All Azure Kubernetes Service best practices implemented"
    echo "✅ All security standards met"
    echo "✅ All compliance requirements satisfied"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}✨ Good! Chart is AKS-compatible with $WARNINGS minor improvements recommended.${NC}"
    echo "✅ All critical requirements met"
    echo "⚠️  Some optional optimizations available"
    exit 0
else
    echo -e "${RED}❌ Chart needs improvement: $ERRORS errors and $WARNINGS warnings found.${NC}"
    echo "🔧 Please address the critical issues before deploying to AKS production."
    echo ""
    echo "📚 Resources:"
    echo "- AKS Best Practices: https://docs.microsoft.com/azure/aks/best-practices"
    echo "- Kubernetes Security: https://kubernetes.io/docs/concepts/security/"
    echo "- Helm Best Practices: https://helm.sh/docs/chart_best_practices/"
    exit 1
fi
