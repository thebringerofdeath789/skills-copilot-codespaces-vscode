"""
Cost Calculator Tab
Comprehensive cost analysis and ROI calculations
"""

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from typing import Dict, Any
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use('Agg')  # Use non-interactive backend

from core.calculators.cost_calculator import CostCalculator
from data.knowledge_base.products import product_database

class CostCalculatorTab(ctk.CTkFrame):
    """Advanced cost calculation interface"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.cost_calculator = CostCalculator()
        self.current_analysis = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the cost calculator interface"""
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(header_frame, text="Cost Calculator & ROI Analysis", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(side="left", padx=10, pady=10)
        
        # Calculation mode selector
        self.calc_mode = ctk.CTkOptionMenu(header_frame,
                                          values=["Setup Cost Analysis", "Operating Cost Analysis", 
                                                 "ROI Analysis", "Setup Comparison"],
                                          command=self.on_mode_change)
        self.calc_mode.pack(side="right", padx=10, pady=10)
        
        # Main content area (scrollable)
        self.content_frame = ctk.CTkScrollableFrame(main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Initialize with setup cost analysis
        self.show_setup_cost_analysis()
    
    def on_mode_change(self, mode):
        """Handle calculation mode change"""
        
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if mode == "Setup Cost Analysis":
            self.show_setup_cost_analysis()
        elif mode == "Operating Cost Analysis":
            self.show_operating_cost_analysis()
        elif mode == "ROI Analysis":
            self.show_roi_analysis()
        elif mode == "Setup Comparison":
            self.show_setup_comparison()
    
    def show_setup_cost_analysis(self):
        """Show setup cost analysis interface"""
        
        # Input parameters frame
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(input_frame, text="Setup Configuration", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 20))
        
        # Parameter grid
        param_frame = ctk.CTkFrame(input_frame)
        param_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Tent size
        ctk.CTkLabel(param_frame, text="Tent Size:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.tent_size_var = ctk.CTkOptionMenu(param_frame, 
                                              values=["2x2", "2x4", "4x4", "4x8"])
        self.tent_size_var.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        # Lighting wattage
        ctk.CTkLabel(param_frame, text="Lighting:").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.lighting_var = ctk.CTkOptionMenu(param_frame,
                                             values=["100w", "150w", "240w", "320w"])
        self.lighting_var.grid(row=0, column=3, sticky="ew", padx=10, pady=5)
        
        # Ventilation tier
        ctk.CTkLabel(param_frame, text="Ventilation:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.ventilation_var = ctk.CTkOptionMenu(param_frame,
                                                values=["4inch_basic", "4inch_premium", 
                                                       "6inch_basic", "6inch_premium"])
        self.ventilation_var.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Growing method
        ctk.CTkLabel(param_frame, text="Growing Medium:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        self.growing_method_var = ctk.CTkOptionMenu(param_frame,
                                                   values=["soil", "coco", "hydroponic"])
        self.growing_method_var.grid(row=1, column=3, sticky="ew", padx=10, pady=5)
        
        # Configure grid weights
        param_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        # Calculate button
        calc_button = ctk.CTkButton(input_frame, text="Calculate Setup Costs",
                                   command=self.calculate_setup_costs)
        calc_button.pack(pady=10)
        
        # Results frame
        self.setup_results_frame = ctk.CTkFrame(self.content_frame)
        self.setup_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(self.setup_results_frame, text="Cost Breakdown", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.setup_results_content = ctk.CTkFrame(self.setup_results_frame)
        self.setup_results_content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def calculate_setup_costs(self):
        """Calculate and display setup costs"""
        
        try:
            # Get parameters
            tent_size = self.tent_size_var.get()
            lighting = self.lighting_var.get()
            ventilation = self.ventilation_var.get()
            growing_method = self.growing_method_var.get()
            
            # Calculate costs
            setup_costs = self.cost_calculator.calculate_setup_costs(
                tent_size=tent_size,
                lighting_wattage=lighting,
                ventilation_tier=ventilation,
                growing_method=growing_method
            )
            
            self.display_setup_costs(setup_costs)
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {str(e)}")
    
    def display_setup_costs(self, costs_data):
        """Display setup cost breakdown"""
        
        # Clear previous results
        for widget in self.setup_results_content.winfo_children():
            widget.destroy()
        
        # Cost breakdown table
        breakdown_frame = ctk.CTkFrame(self.setup_results_content)
        breakdown_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(breakdown_frame, text="Equipment Cost Breakdown", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Headers
        header_frame = ctk.CTkFrame(breakdown_frame, fg_color="gray30")
        header_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        ctk.CTkLabel(header_frame, text="Component", width=150).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(header_frame, text="Min Cost", width=80).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(header_frame, text="Avg Cost", width=80).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(header_frame, text="Max Cost", width=80).pack(side="left", padx=10, pady=5)
        
        # Cost rows
        for component, cost_range in costs_data["cost_breakdown"].items():
            row_frame = ctk.CTkFrame(breakdown_frame)
            row_frame.pack(fill="x", padx=10, pady=1)
            
            ctk.CTkLabel(row_frame, text=component.replace("_", " ").title(), width=150).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(row_frame, text=f"${cost_range['min']}", width=80).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(row_frame, text=f"${cost_range['avg']}", width=80).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(row_frame, text=f"${cost_range['max']}", width=80).pack(side="left", padx=10, pady=5)
        
        # Total costs
        total_frame = ctk.CTkFrame(breakdown_frame, fg_color="gray20")
        total_frame.pack(fill="x", padx=10, pady=10)
        
        total_range = costs_data["total_range"]
        ctk.CTkLabel(total_frame, text="TOTAL SETUP COST", 
                    font=ctk.CTkFont(weight="bold"), width=150).pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(total_frame, text=f"${total_range['min']}", 
                    font=ctk.CTkFont(weight="bold"), width=80).pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(total_frame, text=f"${total_range['avg']}", 
                    font=ctk.CTkFont(weight="bold"), width=80).pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(total_frame, text=f"${total_range['max']}", 
                    font=ctk.CTkFont(weight="bold"), width=80).pack(side="left", padx=10, pady=10)
        
        # Additional info
        info_frame = ctk.CTkFrame(self.setup_results_content)
        info_frame.pack(fill="x", pady=10)
        
        config = costs_data["setup_configuration"]
        plant_capacity = config["estimated_plant_capacity"]
        cost_per_plant = costs_data["cost_per_plant"]
        
        info_text = f"""
Configuration Summary:
• Tent Size: {config['tent_size']}
• Lighting: {config['lighting']}
• Ventilation: {config['ventilation']}
• Growing Method: {config['growing_method']}
• Plant Capacity: {plant_capacity} plants
• Cost per Plant: ${cost_per_plant['min']} - ${cost_per_plant['max']}
        """
        
        info_label = ctk.CTkLabel(info_frame, text=info_text.strip(), 
                                 justify="left", anchor="w")
        info_label.pack(padx=10, pady=10)
    
    def show_operating_cost_analysis(self):
        """Show operating cost analysis interface"""
        
        # Input parameters
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(input_frame, text="Operating Cost Parameters", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 20))
        
        param_frame = ctk.CTkFrame(input_frame)
        param_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Plant count
        ctk.CTkLabel(param_frame, text="Number of Plants:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.plant_count_var = ctk.CTkEntry(param_frame, width=100)
        self.plant_count_var.insert(0, "4")
        self.plant_count_var.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Lighting schedule
        ctk.CTkLabel(param_frame, text="Lighting Schedule:").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.lighting_schedule_var = ctk.CTkOptionMenu(param_frame,
                                                      values=["18h vegetative", "12h flowering"])
        self.lighting_schedule_var.grid(row=0, column=3, sticky="ew", padx=10, pady=5)
        
        # Cycles per year
        ctk.CTkLabel(param_frame, text="Cycles per Year:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.cycles_var = ctk.CTkEntry(param_frame, width=100)
        self.cycles_var.insert(0, "3")
        self.cycles_var.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Location tier (affects electricity costs)
        ctk.CTkLabel(param_frame, text="Location:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        self.location_var = ctk.CTkOptionMenu(param_frame,
                                             values=["low_cost", "average", "high_cost"])
        self.location_var.grid(row=1, column=3, sticky="ew", padx=10, pady=5)
        
        param_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        # Calculate button
        calc_button = ctk.CTkButton(input_frame, text="Calculate Operating Costs",
                                   command=self.calculate_operating_costs)
        calc_button.pack(pady=10)
        
        # Results frame
        self.operating_results_frame = ctk.CTkFrame(self.content_frame)
        self.operating_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(self.operating_results_frame, text="Operating Cost Analysis", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.operating_results_content = ctk.CTkFrame(self.operating_results_frame)
        self.operating_results_content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def calculate_operating_costs(self):
        """Calculate and display operating costs"""
        
        try:
            plant_count = int(self.plant_count_var.get())
            lighting_schedule = self.lighting_schedule_var.get()
            cycles_per_year = int(self.cycles_var.get())
            location = self.location_var.get()
            
            operating_costs = self.cost_calculator.calculate_operating_costs(
                lighting_schedule=lighting_schedule,
                plant_count=plant_count,
                cycles_per_year=cycles_per_year,
                location_tier=location
            )
            
            self.display_operating_costs(operating_costs)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for plant count and cycles")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {str(e)}")
    
    def display_operating_costs(self, costs_data):
        """Display operating cost breakdown"""
        
        # Clear previous results
        for widget in self.operating_results_content.winfo_children():
            widget.destroy()
        
        # Monthly costs
        monthly_frame = ctk.CTkFrame(self.operating_results_content)
        monthly_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(monthly_frame, text="Monthly Operating Costs", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        monthly_costs = costs_data["monthly_costs"]
        for cost_type, amount in monthly_costs.items():
            cost_frame = ctk.CTkFrame(monthly_frame)
            cost_frame.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(cost_frame, text=cost_type.replace("_", " ").title(), 
                        width=200).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(cost_frame, text=f"${amount}", 
                        width=100).pack(side="right", padx=10, pady=5)
        
        # Annual costs
        annual_frame = ctk.CTkFrame(self.operating_results_content)
        annual_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(annual_frame, text="Annual Operating Costs", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        annual_costs = costs_data["annual_costs"]
        for cost_type, amount in annual_costs.items():
            cost_frame = ctk.CTkFrame(annual_frame)
            cost_frame.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(cost_frame, text=cost_type.replace("_", " ").title(), 
                        width=200).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(cost_frame, text=f"${amount}", 
                        width=100).pack(side="right", padx=10, pady=5)
        
        # Cost per plant
        summary_frame = ctk.CTkFrame(self.operating_results_content, fg_color="gray20")
        summary_frame.pack(fill="x", pady=10)
        
        cost_per_plant = costs_data["cost_per_plant_per_year"]
        ctk.CTkLabel(summary_frame, text=f"Annual Cost per Plant: ${cost_per_plant}", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
    
    def show_roi_analysis(self):
        """Show ROI analysis interface"""
        
        # Input parameters
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(input_frame, text="ROI Analysis Parameters", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 20))
        
        param_frame = ctk.CTkFrame(input_frame)
        param_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Setup selection
        ctk.CTkLabel(param_frame, text="Setup Type:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.roi_tent_size = ctk.CTkOptionMenu(param_frame, 
                                              values=["2x2", "2x4", "4x4", "4x8"])
        self.roi_tent_size.set("2x4")
        self.roi_tent_size.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        # Experience level
        ctk.CTkLabel(param_frame, text="Experience Level:").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.experience_var = ctk.CTkOptionMenu(param_frame,
                                               values=["beginner", "intermediate", "advanced"])
        self.experience_var.set("intermediate")
        self.experience_var.grid(row=0, column=3, sticky="ew", padx=10, pady=5)
        
        param_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        # Calculate button
        calc_button = ctk.CTkButton(input_frame, text="Calculate ROI Analysis",
                                   command=self.calculate_roi_analysis)
        calc_button.pack(pady=10)
        
        # Results frame
        self.roi_results_frame = ctk.CTkFrame(self.content_frame)
        self.roi_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(self.roi_results_frame, text="ROI Analysis Results", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.roi_results_content = ctk.CTkFrame(self.roi_results_frame)
        self.roi_results_content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def calculate_roi_analysis(self):
        """Calculate and display ROI analysis"""
        
        try:
            tent_size = self.roi_tent_size.get()
            experience = self.experience_var.get()
            
            # Get setup costs
            setup_costs = self.cost_calculator.calculate_setup_costs(
                tent_size=tent_size,
                lighting_wattage="150w",
                ventilation_tier="4inch_basic",
                growing_method="soil"
            )
            
            # Get operating costs (estimate 4 plants for 2x4, adjust for other sizes)
            plant_multiplier = {"2x2": 0.5, "2x4": 1.0, "4x4": 2.25, "4x8": 4.0}
            plant_count = int(4 * plant_multiplier.get(tent_size, 1.0))
            
            operating_costs = self.cost_calculator.calculate_operating_costs(
                lighting_schedule="12h flowering",
                plant_count=plant_count,
                cycles_per_year=3
            )
            
            # Calculate ROI
            roi_analysis = self.cost_calculator.calculate_roi_analysis(
                setup_costs=setup_costs,
                operating_costs=operating_costs,
                tent_size=tent_size,
                experience_level=experience
            )
            
            self.display_roi_analysis(roi_analysis)
            
        except Exception as e:
            messagebox.showerror("Error", f"ROI calculation failed: {str(e)}")
    
    def display_roi_analysis(self, roi_data):
        """Display ROI analysis results"""
        
        # Clear previous results
        for widget in self.roi_results_content.winfo_children():
            widget.destroy()
        
        # Investment summary
        investment_frame = ctk.CTkFrame(self.roi_results_content)
        investment_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(investment_frame, text="Investment Summary", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        setup_cost = roi_data["setup_investment"]
        annual_operating = roi_data["annual_operating_costs"]
        
        investment_info = f"""
Initial Setup Investment: ${setup_cost:,.2f}
Annual Operating Costs: ${annual_operating:,.2f}
        """
        
        ctk.CTkLabel(investment_frame, text=investment_info.strip(), 
                    justify="left").pack(padx=10, pady=(0, 10))
        
        # Yield analysis
        yield_frame = ctk.CTkFrame(self.roi_results_content)
        yield_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(yield_frame, text="Yield Analysis", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        yield_data = roi_data["yield_analysis"]
        yield_info = f"""
Annual Yield: {yield_data['annual_yield_grams']:.1f} grams ({yield_data['annual_yield_ounces']:.1f} oz)
Market Value: ${yield_data['market_value_per_gram']:.2f} per gram
Total Annual Value: ${yield_data['annual_market_value']:,.2f}
        """
        
        ctk.CTkLabel(yield_frame, text=yield_info.strip(), 
                    justify="left").pack(padx=10, pady=(0, 10))
        
        # Profitability analysis
        profit_frame = ctk.CTkFrame(self.roi_results_content, fg_color="gray20")
        profit_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(profit_frame, text="Profitability Analysis", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        profitability = roi_data["profitability"]
        profit_info = f"""
Annual Net Profit: ${profitability['annual_net_profit']:,.2f}
Profit Margin: {profitability['profit_margin']:.1f}%
Payback Period: {profitability['payback_period_years']} years
        """
        
        ctk.CTkLabel(profit_frame, text=profit_info.strip(), 
                    justify="left", font=ctk.CTkFont(weight="bold")).pack(padx=10, pady=(0, 10))
        
        # 3-year projection
        projection_frame = ctk.CTkFrame(self.roi_results_content)
        projection_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(projection_frame, text="3-Year Projection", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        projection = roi_data["three_year_projection"]
        projection_info = f"""
Total Investment (3 years): ${projection['total_investment']:,.2f}
Total Operating Costs: ${projection['total_operating_costs']:,.2f}
Total Market Value: ${projection['total_market_value']:,.2f}
Net Profit (3 years): ${projection['net_profit']:,.2f}
ROI Percentage: {projection['roi_percentage']:.1f}%
        """
        
        ctk.CTkLabel(projection_frame, text=projection_info.strip(), 
                    justify="left").pack(padx=10, pady=(0, 10))
        
        # Cost per gram analysis
        cost_frame = ctk.CTkFrame(self.roi_results_content)
        cost_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(cost_frame, text="Cost per Gram Breakdown", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        cost_per_gram = roi_data["cost_per_gram"]
        cost_info = f"""
Setup Cost per Gram: ${cost_per_gram['setup_cost_per_gram']:.2f}
Operating Cost per Gram: ${cost_per_gram['operating_cost_per_gram']:.2f}
Total Cost per Gram: ${cost_per_gram['total_cost_per_gram']:.2f}
        """
        
        ctk.CTkLabel(cost_frame, text=cost_info.strip(), 
                    justify="left").pack(padx=10, pady=(0, 10))
    
    def show_setup_comparison(self):
        """Show setup comparison interface"""
        
        # Comparison parameters
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(input_frame, text="Setup Comparison", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 20))
        
        # Experience level
        param_frame = ctk.CTkFrame(input_frame)
        param_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(param_frame, text="Experience Level:").pack(side="left", padx=10, pady=10)
        self.comparison_experience = ctk.CTkOptionMenu(param_frame,
                                                      values=["beginner", "intermediate", "advanced"])
        self.comparison_experience.set("intermediate")
        self.comparison_experience.pack(side="left", padx=10, pady=10)
        
        # Calculate button
        calc_button = ctk.CTkButton(input_frame, text="Compare All Setup Options",
                                   command=self.calculate_setup_comparison)
        calc_button.pack(pady=10)
        
        # Results frame
        self.comparison_results_frame = ctk.CTkFrame(self.content_frame)
        self.comparison_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(self.comparison_results_frame, text="Setup Comparison Results", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.comparison_results_content = ctk.CTkScrollableFrame(self.comparison_results_frame)
        self.comparison_results_content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def calculate_setup_comparison(self):
        """Calculate and display setup comparison"""
        
        try:
            experience = self.comparison_experience.get()
            tent_sizes = ["2x2", "2x4", "4x4", "4x8"]
            
            comparison = self.cost_calculator.compare_setup_options(
                tent_sizes=tent_sizes,
                experience_level=experience
            )
            
            self.display_setup_comparison(comparison)
            
        except Exception as e:
            messagebox.showerror("Error", f"Comparison calculation failed: {str(e)}")
    
    def display_setup_comparison(self, comparison_data):
        """Display setup comparison results"""
        
        # Clear previous results
        for widget in self.comparison_results_content.winfo_children():
            widget.destroy()
        
        # Comparison table
        table_frame = ctk.CTkFrame(self.comparison_results_content)
        table_frame.pack(fill="x", pady=10)
        
        # Headers
        header_frame = ctk.CTkFrame(table_frame, fg_color="gray30")
        header_frame.pack(fill="x", padx=5, pady=(5, 2))
        
        headers = ["Tent Size", "Setup Cost", "Annual Op.", "Annual Yield", "Annual Profit", "Payback", "3-Yr ROI%"]
        header_widths = [80, 90, 90, 90, 90, 80, 80]
        
        for header, width in zip(headers, header_widths):
            ctk.CTkLabel(header_frame, text=header, width=width, 
                        font=ctk.CTkFont(weight="bold")).pack(side="left", padx=2, pady=5)
        
        # Data rows
        for i, result in enumerate(comparison_data["comparison_results"]):
            row_color = "gray20" if i == 0 else "transparent"  # Highlight best option
            row_frame = ctk.CTkFrame(table_frame, fg_color=row_color)
            row_frame.pack(fill="x", padx=5, pady=1)
            
            values = [
                result["tent_size"],
                f"${result['setup_cost']:,.0f}",
                f"${result['annual_operating']:,.0f}",
                f"{result['annual_yield_grams']:.0f}g",
                f"${result['annual_profit']:,.0f}",
                f"{result['payback_years']} yr" if result['payback_years'] != 'N/A' else 'N/A',
                f"{result['three_year_roi']:.0f}%"
            ]
            
            for value, width in zip(values, header_widths):
                font_weight = "bold" if i == 0 else "normal"
                ctk.CTkLabel(row_frame, text=value, width=width,
                           font=ctk.CTkFont(weight=font_weight)).pack(side="left", padx=2, pady=5)
        
        # Best option summary
        if comparison_data["best_roi"]:
            best_frame = ctk.CTkFrame(self.comparison_results_content, fg_color="green")
            best_frame.pack(fill="x", pady=10)
            
            best = comparison_data["best_roi"]
            summary_text = f"""
RECOMMENDED SETUP: {best['tent_size']} Tent
• Highest 3-Year ROI: {best['three_year_roi']:.1f}%
• Annual Profit: ${best['annual_profit']:,.2f}
• Payback Period: {best['payback_years']} years
            """
            
            ctk.CTkLabel(best_frame, text=summary_text.strip(), 
                        justify="left", font=ctk.CTkFont(weight="bold")).pack(padx=10, pady=10)

import customtkinter as ctk
import logging
from config.themes import themes

class CostCalculatorTab:
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            parent,
            text="💰 Cost Calculator & Analytics\n\nComprehensive financial analysis and ROI tracking\nComing soon...",
            font=ctk.CTkFont(size=16)
        )
        label.grid(row=0, column=0, padx=20, pady=20)
