#!/bin/bash

# Enhanced Helm Chart Validation Script
# This script validates the Helm chart template for production readiness,
# security compliance, and regulatory standards

set -e

CHART_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERRORS=0
WARNINGS=0

echo "🔍 Enhanced Helm Chart Validation..."
echo "Chart directory: $CHART_DIR"
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    fi
}

# Security validation
validate_security() {
    echo "🔒 Security Validation..."
    
    # Check for Pod Security Standards
    if grep -q "podSecurityStandards:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Pod Security Standards configuration found"
    else
        print_status "FAIL" "Pod Security Standards configuration missing"
    fi
    
    # Check for security contexts
    if grep -q "runAsNonRoot: true" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Non-root security context configured"
    else
        print_status "FAIL" "Non-root security context not configured"
    fi
    
    # Check for network policies
    if grep -q "networkPolicy:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Network policy configuration found"
    else
        print_status "FAIL" "Network policy configuration missing"
    fi
    
    # Check for Azure Key Vault integration
    if grep -q "azureKeyVault:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Azure Key Vault integration configured"
    else
        print_status "WARN" "Azure Key Vault integration not configured"
    fi
    
    # Check for RBAC
    if grep -q "rbac:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "RBAC configuration found"
    else
        print_status "WARN" "RBAC configuration missing"
    fi
}

# Compliance validation
validate_compliance() {
    echo "📋 Compliance Validation..."
    
    # Check for compliance configuration
    if grep -q "compliance:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Compliance configuration found"
    else
        print_status "FAIL" "Compliance configuration missing"
    fi
    
    # Check for audit logging
    if grep -q "auditLogging:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Audit logging configuration found"
    else
        print_status "FAIL" "Audit logging configuration missing"
    fi
    
    # Check for resource governance
    if grep -q "resourceQuota:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Resource quota configuration found"
    else
        print_status "WARN" "Resource quota configuration missing"
    fi
    
    if grep -q "limitRange:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Limit range configuration found"
    else
        print_status "WARN" "Limit range configuration missing"
    fi
}

# Production readiness validation
validate_production_readiness() {
    echo "🚀 Production Readiness Validation..."
    
    # Check for resource limits
    if grep -q "resources:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Resource management configuration found"
    else
        print_status "FAIL" "Resource management configuration missing"
    fi
    
    # Check for health checks
    if grep -q "livenessProbe:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Liveness probe configuration found"
    else
        print_status "FAIL" "Liveness probe configuration missing"
    fi
    
    if grep -q "readinessProbe:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Readiness probe configuration found"
    else
        print_status "FAIL" "Readiness probe configuration missing"
    fi
    
    # Check for autoscaling
    if grep -q "autoscaling:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Autoscaling configuration found"
    else
        print_status "WARN" "Autoscaling configuration missing"
    fi
    
    # Check for Pod Disruption Budget
    if grep -q "podDisruptionBudget:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Pod Disruption Budget configuration found"
    else
        print_status "WARN" "Pod Disruption Budget configuration missing"
    fi
    
    # Check for monitoring
    if grep -q "monitoring:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "Monitoring configuration found"
    else
        print_status "FAIL" "Monitoring configuration missing"
    fi
}

# Template validation
validate_templates() {
    echo "📄 Template Validation..."
    
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
    )
    
    for template in "${required_templates[@]}"; do
        if [ -f "$CHART_DIR/$template" ]; then
            print_status "PASS" "Template exists: $template"
        else
            print_status "FAIL" "Missing template: $template"
        fi
    done
}

# Run all validations
validate_security
echo
validate_compliance
echo
validate_production_readiness
echo
validate_templates
echo

# Summary
echo "📊 Validation Summary"
echo "===================="
echo "Total Errors: $ERRORS"
echo "Total Warnings: $WARNINGS"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}🎉 All validations passed! Chart is production-ready.${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Chart passed with $WARNINGS warnings. Review recommended.${NC}"
    exit 0
else
    echo -e "${RED}❌ Chart failed validation with $ERRORS errors and $WARNINGS warnings.${NC}"
    echo "Please address the issues before deploying to production."
    exit 1
fi

# Check if required files exist
echo "📁 Checking required files..."
required_files=(
    "Chart.yaml"
    "values.yaml"
    ".helmignore"
    "README.md"
    "templates/_helpers.tpl"
    "templates/deployment.yaml"
    "templates/service.yaml"
    "templates/serviceaccount.yaml"
    "templates/ingress.yaml"
    "templates/NOTES.txt"
)

for file in "${required_files[@]}"; do
    if [ -f "$CHART_DIR/$file" ]; then
        print_status "PASS" "Required file exists: $file"
    else
        print_status "FAIL" "Missing required file: $file"
    fi
done

# Check environment files
echo
echo "🌍 Checking environment files..."
env_files=(
    "environments/values.dev.yaml"
    "environments/values.staging.yaml"
    "environments/values.prod.yaml"
)

for file in "${env_files[@]}"; do
    if [ -f "$CHART_DIR/$file" ]; then
        print_status "PASS" "Environment file exists: $file"
    else
        print_status "FAIL" "Missing environment file: $file"
    fi
done

# Check documentation files
echo
echo "📚 Checking documentation files..."
doc_files=(
    "docs/CONFIGURATION.md"
    "docs/AZURE_INTEGRATION.md"
    "docs/ENVIRONMENTS.md"
    "docs/EXAMPLES.md"
)

for file in "${doc_files[@]}"; do
    if [ -f "$CHART_DIR/$file" ]; then
        print_status "PASS" "Documentation file exists: $file"
    else
        print_status "FAIL" "Missing documentation file: $file"
    fi
done

# Validate Chart.yaml
echo
echo "📊 Validating Chart.yaml..."
if [ -f "$CHART_DIR/Chart.yaml" ]; then
    # Check for required fields
    if grep -q "^name:" "$CHART_DIR/Chart.yaml"; then
        print_status "PASS" "Chart.yaml contains name field"
    else
        print_status "FAIL" "Chart.yaml missing name field"
    fi
    
    if grep -q "^version:" "$CHART_DIR/Chart.yaml"; then
        print_status "PASS" "Chart.yaml contains version field"
    else
        print_status "FAIL" "Chart.yaml missing version field"
    fi
    
    if grep -q "^apiVersion:" "$CHART_DIR/Chart.yaml"; then
        print_status "PASS" "Chart.yaml contains apiVersion field"
    else
        print_status "FAIL" "Chart.yaml missing apiVersion field"
    fi
fi

# Validate Helm template syntax
echo
echo "🔧 Validating Helm template syntax..."
if command -v helm &> /dev/null; then
    # Test template rendering with default values
    if helm template test-release "$CHART_DIR" --values "$CHART_DIR/values.yaml" > /dev/null 2>&1; then
        print_status "PASS" "Helm template renders successfully with default values"
    else
        print_status "FAIL" "Helm template fails to render with default values"
    fi
    
    # Test with environment files
    for env in dev staging prod; do
        if [ -f "$CHART_DIR/environments/values.$env.yaml" ]; then
            if helm template test-release "$CHART_DIR" \
                --values "$CHART_DIR/values.yaml" \
                --values "$CHART_DIR/environments/values.$env.yaml" > /dev/null 2>&1; then
                print_status "PASS" "Helm template renders successfully with $env values"
            else
                print_status "FAIL" "Helm template fails to render with $env values"
            fi
        fi
    done
    
    # Validate chart
    if helm lint "$CHART_DIR" > /dev/null 2>&1; then
        print_status "PASS" "Helm chart passes lint check"
    else
        print_status "FAIL" "Helm chart fails lint check"
    fi
else
    print_status "WARN" "Helm CLI not found, skipping template validation"
fi

# Check for security best practices
echo
echo "🔒 Checking security best practices..."
if [ -f "$CHART_DIR/values.yaml" ]; then
    # Check for security context
    if grep -q "securityContext:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "values.yaml includes securityContext configuration"
    else
        print_status "WARN" "values.yaml missing securityContext configuration"
    fi
    
    # Check for resource limits
    if grep -q "resources:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "values.yaml includes resource configuration"
    else
        print_status "WARN" "values.yaml missing resource configuration"
    fi
    
    # Check for network policy
    if grep -q "networkPolicy:" "$CHART_DIR/values.yaml"; then
        print_status "PASS" "values.yaml includes networkPolicy configuration"
    else
        print_status "WARN" "values.yaml missing networkPolicy configuration"
    fi
fi

# Check template files for best practices
echo
echo "📋 Checking template best practices..."
if [ -f "$CHART_DIR/templates/deployment.yaml" ]; then
    # Check for readiness probe
    if grep -q "readinessProbe:" "$CHART_DIR/templates/deployment.yaml"; then
        print_status "PASS" "Deployment template includes readiness probe"
    else
        print_status "WARN" "Deployment template missing readiness probe"
    fi
    
    # Check for liveness probe
    if grep -q "livenessProbe:" "$CHART_DIR/templates/deployment.yaml"; then
        print_status "PASS" "Deployment template includes liveness probe"
    else
        print_status "WARN" "Deployment template missing liveness probe"
    fi
    
    # Check for security context
    if grep -q "securityContext:" "$CHART_DIR/templates/deployment.yaml"; then
        print_status "PASS" "Deployment template includes security context"
    else
        print_status "WARN" "Deployment template missing security context"
    fi
fi

# Check for Kubernetes API versions
echo
echo "🔄 Checking Kubernetes API versions..."
template_files=("$CHART_DIR"/templates/*.yaml)
for file in "${template_files[@]}"; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        if grep -q "apiVersion:" "$file"; then
            # Check for deprecated API versions
            if grep -q "apiVersion: extensions/v1beta1" "$file"; then
                print_status "WARN" "$filename uses deprecated extensions/v1beta1 API"
            elif grep -q "apiVersion: apps/v1beta" "$file"; then
                print_status "WARN" "$filename uses deprecated apps/v1beta API"
            else
                print_status "PASS" "$filename uses current API versions"
            fi
        fi
    fi
done

# Check values.yaml structure
echo
echo "📝 Checking values.yaml structure..."
if [ -f "$CHART_DIR/values.yaml" ]; then
    # Check for common sections
    sections=("image" "service" "ingress" "resources" "autoscaling" "serviceAccount")
    for section in "${sections[@]}"; do
        if grep -q "^$section:" "$CHART_DIR/values.yaml"; then
            print_status "PASS" "values.yaml contains $section section"
        else
            print_status "WARN" "values.yaml missing $section section"
        fi
    done
fi

# Final summary
echo
echo "📊 Validation Summary"
echo "===================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Validation completed successfully with no critical errors!${NC}"
    echo "The Helm chart template is ready for use."
else
    echo -e "${RED}❌ Validation completed with $ERRORS error(s).${NC}"
    echo "Please fix the errors before using the chart template."
fi

echo
echo "📖 Next Steps:"
echo "1. Customize values.yaml for your application"
echo "2. Update environment-specific values in environments/ directory"
echo "3. Test deployment with: helm install my-app . --values values.yaml"
echo "4. Read the documentation in docs/ directory for detailed configuration"

exit $ERRORS
