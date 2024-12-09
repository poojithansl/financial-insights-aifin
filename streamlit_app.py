import streamlit as st
# from system import RAGSystem

# TODO: develop a Streamlit-based web application that enables
# users to ask questions about a company's financial statements
# for a specific year. The app should include dropdown menus for
# selecting the company ticker and year, alongside a text box for
# entering queries. Responses will be generated using a prebuilt
# Retrieval-Augmented Generation (RAG) pipeline.

# The application must be robust and should never crash, handling
# all errors gracefully with user-friendly messages. It should
# ensure a smooth user experience, even when unexpected issues
# occur during execution.

import traceback


class RAG_System2():
    def __init__(self):
        pass
    
    def respond(self, query, ticker, year):
        return f"Answering query for {query}, year - {year}, ticker - {ticker}", None



class RAGApp:
    def __init__(self):
        # Initialize the RAG system
        self._rag_system = RAG_System2()
        
        # Define list of tickers and years (you might want to populate this dynamically)
        self._tickers = [
            'EQIX',  # Example ticker
            'FRT',   # Example ticker
            'PARA',  # Example ticker
            'PCG',   # Example ticker
            'PGR',   # Example ticker
            'TROW',  # Example ticker
            'TXT',   # Example ticker
            'UNH',   # Example ticker
            'WTW',   # Example ticker
            'WYNN',  # Example ticker
        ]
        self._years = list(range(2010, 2020))  # Example years from 2010 to 2019

    def _validate_input(self, ticker, year, query):
        """
        Validate user inputs before processing
        """
        if not ticker:
            st.error("Please select a company ticker.")
            return False
        if not year:
            st.error("Please select a year.")
            return False
        if not query:
            st.error("Please enter a query.")
            return False
        return True

    def run(self):
        """
        Main Streamlit application
        """
        # Set page configuration
        st.set_page_config(
            page_title="Financial Statement Query Assistant", 
            page_icon="📊",
            layout="wide"
        )

        # Title and description
        st.title("Financial Statement Query Assistant")
        st.markdown("""
        Ask questions about a company's financial statements. 
        Select a company ticker, year, and enter your query to get insights.
        """)

        # Create columns for input
        col1, col2 = st.columns(2)

        with col1:
            # Ticker selection
            ticker = st.selectbox(
                "Select Company Ticker", 
                options=[''] + self._tickers,
                index=0
            )

        with col2:
            # Year selection
            year = st.selectbox(
                "Select Year", 
                options=[''] + self._years,
                index=0
            )

        # Query input
        query = st.text_input("Enter your query about the financial statement:")

        # Submit button
        if st.button("Get Insights", type="primary"):
            # Reset previous outputs
            st.session_state.response = None
            st.session_state.source_nodes = None

            try:
                # Validate inputs
                if not self._validate_input(ticker, year, query):
                    return

                # Perform query with error handling
                with st.spinner('Analyzing financial statement...'):
                    # Call RAG system
                    response, source_node = self._rag_system.respond(query, ticker, year)

                    # Store results in session state
                    st.session_state.response = response
                    st.session_state.source_nodes = source_node

                # Display response
                st.success("Insights Retrieved Successfully!")
                st.markdown("### Response")
                st.write(response)

                # Display source information if available
                if source_node:
                    with st.expander("Source Document Details"):
                        st.markdown("#### Most Relevant Source")
                        st.write(f"**Node ID:** {source_node.node.id_}")
                        st.text_area(
                            "Source Text (First 500 characters)", 
                            value=source_node.node.text[:500], 
                            height=200
                        )
                        st.write(f"**Relevance Score:** {source_node.score}")

            except Exception as e:
                # Comprehensive error handling
                st.error("An unexpected error occurred.")
                
                # Provide details for debugging
                with st.expander("Error Details"):
                    st.write("Error Message:", str(e))
                    st.code(traceback.format_exc())
                
                # Log the error (you might want to implement proper logging)
                st.info("Our team has been notified. Please try again later.")

        # Additional information section
        st.markdown("---")
        st.markdown("""
        ### How to Use
        1. Select a company ticker
        2. Choose a year
        3. Enter your query about the financial statement
        4. Click "Get Insights"

        *Insights are generated using advanced AI-powered retrieval and generation techniques.*
        """)

def main():
    app = RAGApp()
    app.run()

if __name__ == '__main__':
    main()
