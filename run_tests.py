#!/usr/bin/env python
"""
Test runner script for StegnoX

This script runs all tests for the StegnoX project and generates a coverage report.
"""

import os
import sys
import argparse
import unittest
import coverage
import time

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run StegnoX tests')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--e2e', action='store_true', help='Run end-to-end tests only')
    parser.add_argument('--desktop', action='store_true', help='Run desktop tests only')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--html', action='store_true', help='Generate HTML coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    return parser.parse_args()

def run_tests(test_type=None, verbose=False):
    """Run tests of the specified type"""
    loader = unittest.TestLoader()

    if test_type == 'unit':
        print("Running unit tests...")
        start_dir = 'tests'
        pattern = 'test_*.py'
    elif test_type == 'integration':
        print("Running integration tests...")
        start_dir = 'tests/integration'
        pattern = 'test_*.py'
    elif test_type == 'e2e':
        print("Running end-to-end tests...")
        start_dir = 'tests/e2e'
        pattern = 'test_*.py'
    elif test_type == 'desktop':
        print("Running desktop tests...")
        start_dir = 'tests/desktop'
        pattern = 'test_*.py'
    else:
        print("Running all tests...")
        start_dir = 'tests'
        pattern = 'test_*.py'

    suite = loader.discover(start_dir=start_dir, pattern=pattern)

    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)

    return result.wasSuccessful()

def main():
    """Main function"""
    args = parse_args()

    # Determine which tests to run
    run_unit = args.unit or not (args.integration or args.e2e or args.desktop)
    run_integration = args.integration or not (args.unit or args.e2e or args.desktop)
    run_e2e = args.e2e or not (args.unit or args.integration or args.desktop)
    run_desktop = args.desktop or not (args.unit or args.integration or args.e2e)

    # Set up coverage if requested
    if args.coverage:
        cov = coverage.Coverage(
            source=['engine', 'storage', 'queue', 'backend', 'desktop'],
            omit=['*/__pycache__/*', '*/tests/*', '*/venv/*']
        )
        cov.start()

    # Track overall success
    success = True
    start_time = time.time()

    # Run the tests
    if run_unit:
        unit_success = run_tests('unit', args.verbose)
        success = success and unit_success

    if run_integration:
        integration_success = run_tests('integration', args.verbose)
        success = success and integration_success

    if run_e2e:
        e2e_success = run_tests('e2e', args.verbose)
        success = success and e2e_success

    if run_desktop:
        desktop_success = run_tests('desktop', args.verbose)
        success = success and desktop_success

    end_time = time.time()
    print(f"Total test time: {end_time - start_time:.2f} seconds")

    # Generate coverage report if requested
    if args.coverage:
        cov.stop()
        cov.save()

        print("\nCoverage Summary:")
        cov.report()

        if args.html:
            html_dir = os.path.join('coverage_html')
            os.makedirs(html_dir, exist_ok=True)
            cov.html_report(directory=html_dir)
            print(f"HTML coverage report generated in {html_dir}")

    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
